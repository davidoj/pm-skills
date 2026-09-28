#!/usr/bin/env python3
"""Migrate an exported active slice of a Kaibernetic goal tree into Linear.

Reads a JSON export (schema in scripts/README.md), then creates Linear
projects (from initiatives/milestones/areas) and issues (from tasks) via the
GraphQL API. Dry-run by default; pass --apply to execute mutations.

Auth: LINEAR_API_KEY env var. Personal API keys are sent verbatim in the
Authorization header -- NO "Bearer " prefix (Bearer is only for OAuth tokens).
The key is needed even in dry-run, which performs read-only queries to compute
accurate skips.

Idempotent: issues whose description already contains "kaibernetic:<uuid>"
are skipped; projects are matched by name.

Stdlib only. Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from typing import Any

API_URL = "https://api.linear.app/graphql"
MUTATION_SLEEP = 0.4  # rate-limit courtesy between mutations (seconds)
CONTEXT_TRUNCATE_AT = 20_000
PROJECT_KINDS = {"initiative", "milestone", "area"}  # area ~ container -> project too
REQUIRED_LABELS = ("migrated", "needs-you", "blocked")
KB_RE = re.compile(r"kaibernetic:([0-9a-f-]{36})", re.IGNORECASE)

# kaibernetic status -> (Linear workflow state name, extra labels)
STATE_MAP: dict[str, tuple[str, list[str]]] = {
    "active": ("Todo", []),
    "ready": ("Todo", []),
    "in_progress": ("In Progress", []),
    "blocked": ("Todo", ["blocked"]),
    "paused": ("Backlog", []),
    "completed": ("Done", []),
    "archived": ("Canceled", []),
}

ISSUE_CREATE = """mutation($input: IssueCreateInput!) {
  issueCreate(input: $input) { issue { id identifier url } } }"""
ISSUE_UPDATE = """mutation($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) { success } }"""
COMMENT_CREATE = """mutation($input: CommentCreateInput!) {
  commentCreate(input: $input) { success } }"""
PROJECT_CREATE = """mutation($input: ProjectCreateInput!) {
  projectCreate(input: $input) { project { id name url } } }"""
LABEL_CREATE = """mutation($input: IssueLabelCreateInput!) {
  issueLabelCreate(input: $input) { issueLabel { id name } } }"""
TEAM_CREATE = """mutation($input: TeamCreateInput!) {
  teamCreate(input: $input) { team { id key name } } }"""  # key auto-derived from name  # VERIFY


class LinearError(RuntimeError):
    """Raised with the full GraphQL/HTTP error body -- no silent fallbacks."""


def gql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        sys.exit("error: LINEAR_API_KEY is not set")
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": key,  # personal API key: raw, no "Bearer " prefix
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise LinearError(
            f"HTTP {exc.code} from Linear:\n{exc.read().decode(errors='replace')}"
        ) from exc
    if payload.get("errors"):
        raise LinearError("GraphQL errors:\n" + json.dumps(payload["errors"], indent=2))
    return payload["data"]


def mutate(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    """gql() plus a courtesy sleep after every mutation."""
    data = gql(query, variables)
    time.sleep(MUTATION_SLEEP)
    return data


def linear_priority(source: int | None) -> int:
    """Map source priority ints to Linear's 1=Urgent, 2=High, 3=Medium, 4=Low."""
    if source is None:
        return 3
    if source >= 2:
        return 1
    return {1: 2, 0: 3}.get(source, 4)  # anything <= -1 -> Low


def build_description(item: dict[str, Any]) -> str:
    """description + context_md (truncated) + provenance footer."""
    parts: list[str] = []
    if item.get("description"):
        parts.append(str(item["description"]).strip())
    ctx = item.get("context_md") or ""
    if ctx:
        if len(ctx) > CONTEXT_TRUNCATE_AT:
            ctx = ctx[:CONTEXT_TRUNCATE_AT] + (
                "\n\n*(context_md truncated at 20,000 chars during migration; "
                "full text remains in Kaibernetic.)*"
            )
        parts.append(ctx.strip())
    parts.append(
        f"---\nkaibernetic:{item['kaibernetic_id']} · migrated "
        f"{date.today().isoformat()} · [original]({item.get('url', '')})"
    )
    return "\n\n".join(parts)


def resolve_team(team_arg: str, apply: bool) -> dict[str, Any] | None:
    """Find team by key or name; create it under --apply if missing."""
    nodes = gql("query { teams(first: 250) { nodes { id key name } } }")["teams"]["nodes"]
    for team in nodes:
        if team_arg.lower() in (team["key"].lower(), team["name"].lower()):
            print(f"team: using existing {team['key']} ({team['name']})")
            return team
    print(f"team: '{team_arg}' not found -> will create it")
    if not apply:
        return None
    team = mutate(TEAM_CREATE, {"input": {"name": team_arg}})["teamCreate"]["team"]
    print(f"team: created {team['key']} ({team['name']})")
    return team


class Migrator:
    def __init__(self, team: dict[str, Any] | None, apply: bool) -> None:
        self.apply = apply
        self.team_id: str | None = team["id"] if team else None
        self.states: dict[str, str] = {}       # workflow state name -> id
        self.labels: dict[str, str] = {}       # label name -> id
        self.existing: dict[str, dict] = {}    # kaibernetic uuid -> existing issue
        self.projects: dict[str, str] = {}     # project name -> id
        self.issue_ids: dict[str, str] = {}    # migrated item title -> issue id
        self.created = 0
        self.skipped = 0
        self.failed = 0

    # -- read-side preparation -------------------------------------------

    def prepare(self) -> None:
        if self.team_id is None:  # dry-run against a not-yet-created team
            print("plan: team does not exist yet -- nothing to skip, all items are new")
            return
        self.states = {
            n["name"]: n["id"]
            for n in gql(
                "query($id: String!) { team(id: $id) { states { nodes { id name } } } }",
                {"id": self.team_id},
            )["team"]["states"]["nodes"]
        }
        self._ensure_labels()
        self._fetch_migrated()
        self.projects = {
            n["name"]: n["id"]
            for n in gql(
                "query($id: String!) { team(id: $id) {"
                " projects(first: 250) { nodes { id name } } } }",
                {"id": self.team_id},
            )["team"]["projects"]["nodes"]
        }

    def _ensure_labels(self) -> None:
        nodes = gql("query { issueLabels(first: 250) { nodes { id name } } }")[
            "issueLabels"]["nodes"]  # covers workspace + team labels
        have = {n["name"].lower(): n["id"] for n in nodes}
        for name in REQUIRED_LABELS:
            if name.lower() in have:
                self.labels[name] = have[name.lower()]
            elif self.apply:
                data = mutate(LABEL_CREATE, {"input": {"name": name, "teamId": self.team_id}})
                self.labels[name] = data["issueLabelCreate"]["issueLabel"]["id"]
                print(f"label: created '{name}'")
            else:
                print(f"label: would create '{name}'")
                self.labels[name] = f"<pending:{name}>"

    def _fetch_migrated(self) -> None:
        """Index already-migrated issues by their kaibernetic:<uuid> footer."""
        cursor: str | None = None
        while True:
            data = gql(
                "query($teamId: ID!, $after: String) {"
                ' issues(first: 100, after: $after, includeArchived: true,'
                '   filter: { team: { id: { eq: $teamId } },'
                '             description: { contains: "kaibernetic:" } }) {'
                "  nodes { id identifier title description }"
                "  pageInfo { hasNextPage endCursor } } }",
                {"teamId": self.team_id, "after": cursor},
            )["issues"]
            for node in data["nodes"]:
                match = KB_RE.search(node.get("description") or "")
                if match:
                    self.existing[match.group(1).lower()] = node
            if not data["pageInfo"]["hasNextPage"]:
                break
            cursor = data["pageInfo"]["endCursor"]
        if self.existing:
            print(f"idempotency: {len(self.existing)} previously migrated issue(s) found")

    # -- pass 0: projects --------------------------------------------------

    def migrate_project(self, item: dict[str, Any]) -> None:
        title = item["title"]
        if title in self.projects:
            print(f"[skip] project '{title}' already exists")
            self.skipped += 1
            return
        if not self.apply:
            print(f"[plan] project '{title}' (from kind={item['kind']})")
            self.projects[title] = f"<pending:{title}>"
            self.created += 1
            return
        # Project description is a short field; provenance/idempotency for
        # projects is by name, not by uuid footer.
        summary = (item.get("description") or f"Migrated from Kaibernetic ({item['kind']}).")[:240]
        try:
            data = mutate(PROJECT_CREATE, {"input": {
                "name": title, "teamIds": [self.team_id], "description": summary,
            }})
        except LinearError as exc:
            print(f"[fail] project '{title}':\n{exc}")
            self.failed += 1
            return
        project = data["projectCreate"]["project"]
        self.projects[title] = project["id"]
        self.created += 1
        print(f"[ok]   project '{title}' -> {project['url']}")

    # -- pass 1: issues ------------------------------------------------------

    def migrate_issue(self, item: dict[str, Any]) -> tuple[str, str] | None:
        """Create one issue. Returns (issue_id, parent_title) when a parent
        link must be resolved in pass 2, else None."""
        uuid = item["kaibernetic_id"].lower()
        title = item["title"]
        parent_title = item.get("parent_title")

        if uuid in self.existing:
            node = self.existing[uuid]
            print(f"[skip] issue '{title}' already migrated as {node['identifier']}")
            self.issue_ids[title] = node["id"]
            self.skipped += 1
            return None

        status = item.get("status") or "active"
        if status not in STATE_MAP:
            print(f"  warning: unknown status '{status}' on '{title}'; using Todo")
        state_name, extra_labels = STATE_MAP.get(status, ("Todo", []))
        label_names = ["migrated", *extra_labels]
        if item.get("needs_user"):
            label_names.append("needs-you")
        priority = linear_priority(item.get("priority"))
        project_id = self.projects.get(item.get("initiative") or "")

        if not self.apply:
            detail = f"state={state_name} priority={priority} labels={','.join(label_names)}"
            if project_id:
                detail += f" project='{item['initiative']}'"
            n_comments = sum(
                (bool(item.get("recent_progress")), bool(item.get("needs_user")),
                 status == "blocked"))
            print(f"[plan] issue '{title}' {detail} comments={n_comments}")
            self.issue_ids[title] = f"<pending:{title}>"
            self.created += 1
            return (self.issue_ids[title], parent_title) if parent_title else None

        issue_input: dict[str, Any] = {
            "teamId": self.team_id,
            "title": title,
            "description": build_description(item),
            "priority": priority,
            "labelIds": [self.labels[n] for n in label_names],
        }
        if state_id := self._state_id(state_name):
            issue_input["stateId"] = state_id
        if project_id and not project_id.startswith("<"):
            issue_input["projectId"] = project_id
        try:
            issue = mutate(ISSUE_CREATE, {"input": issue_input})["issueCreate"]["issue"]
            self._post_comments(issue["id"], item, status)
        except LinearError as exc:
            print(f"[fail] issue '{title}':\n{exc}")
            self.failed += 1
            return None
        self.issue_ids[title] = issue["id"]
        self.created += 1
        print(f"[ok]   issue '{title}' -> {issue['identifier']}")
        return (issue["id"], parent_title) if parent_title else None

    def _state_id(self, name: str) -> str | None:
        if name in self.states:
            return self.states[name]
        print(f"  warning: workflow state '{name}' missing on team; falling back to 'Todo'")
        if "Todo" in self.states:
            return self.states["Todo"]
        print("  warning: no 'Todo' state either; omitting stateId (team default applies)")
        return None

    def _post_comments(self, issue_id: str, item: dict[str, Any], status: str) -> None:
        if item.get("recent_progress"):
            bullets = "\n".join(f"- {entry}" for entry in item["recent_progress"])
            self._comment(issue_id, f"**Progress history (migrated)**\n\n{bullets}")
        if item.get("needs_user"):
            self._comment(issue_id, f"**Needs you:** {item['needs_user']}")
        if status == "blocked":
            self._comment(issue_id, (
                "**Blocked** — migrated with status `blocked` from Kaibernetic; "
                "see description / progress history for the blocker."))

    def _comment(self, issue_id: str, body: str) -> None:
        mutate(COMMENT_CREATE, {"input": {"issueId": issue_id, "body": body}})

    # -- pass 2: parent links ------------------------------------------------

    def link_parent(self, issue_id: str, parent_title: str) -> None:
        if parent_id := self.issue_ids.get(parent_title):
            if not self.apply:
                print(f"[plan] sub-issue link: -> parent issue '{parent_title}'")
                return
            try:
                mutate(ISSUE_UPDATE, {"id": issue_id, "input": {"parentId": parent_id}})
                print(f"[ok]   sub-issue link: -> parent issue '{parent_title}'")
            except LinearError as exc:
                print(f"[fail] parent link -> '{parent_title}':\n{exc}")
                self.failed += 1
            return
        if project_id := self.projects.get(parent_title):
            # Parent was migrated as a project (initiative/milestone/area).
            if not self.apply:
                print(f"[plan] project link: -> project '{parent_title}'")
                return
            try:
                mutate(ISSUE_UPDATE, {"id": issue_id, "input": {"projectId": project_id}})
                print(f"[ok]   project link: -> project '{parent_title}'")
            except LinearError as exc:
                print(f"[fail] project link -> '{parent_title}':\n{exc}")
                self.failed += 1
            return
        print(f"  warning: parent '{parent_title}' not among migrated items; left unparented")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate a Kaibernetic export into Linear (dry-run by default).")
    parser.add_argument("--input", default="data/export.json", help="export JSON path")
    parser.add_argument("--team", required=True, help="Linear team key or name (created if missing)")
    parser.add_argument("--apply", action="store_true", help="execute mutations (default: dry-run)")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        export = json.load(fh)
    items: list[dict[str, Any]] = export.get("items", [])
    print(f"loaded {len(items)} item(s) from {args.input} "
          f"(exported {export.get('exported_at', '?')})")
    print("mode: APPLY -- mutations will run" if args.apply
          else "mode: DRY-RUN -- printing plan only (pass --apply to execute)")

    team = resolve_team(args.team, args.apply)
    migrator = Migrator(team, args.apply)
    migrator.prepare()

    project_items = [i for i in items if i.get("kind") in PROJECT_KINDS]
    task_items = [i for i in items if i.get("kind") not in PROJECT_KINDS]

    print(f"\n-- projects ({len(project_items)}) --")
    for item in project_items:
        migrator.migrate_project(item)

    print(f"\n-- issues ({len(task_items)}) --")
    pending_parents: list[tuple[str, str]] = []
    for item in task_items:
        if pending := migrator.migrate_issue(item):
            pending_parents.append(pending)

    if pending_parents:
        print(f"\n-- parent links ({len(pending_parents)}) --")
        for issue_id, parent_title in pending_parents:
            migrator.link_parent(issue_id, parent_title)

    print(f"\nsummary: created={migrator.created} "
          f"skipped={migrator.skipped} failed={migrator.failed}")
    return 1 if migrator.failed else 0


if __name__ == "__main__":
    sys.exit(main())
