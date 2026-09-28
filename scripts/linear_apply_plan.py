#!/usr/bin/env python3
"""Apply a reconciliation plan to Linear (GraphQL fallback path from backends/linear.md).

Dry-run by default: reads the current state of the project's issues, prints an orient()
dashboard, matches every plan entry to a live issue (by `kaibernetic:<uuid>` footer, then exact
title, then case-insensitive substring), and prints exactly what would be written. `--apply`
performs the writes. Comments are idempotent on their first line (headline); new issues are
skipped if an issue with the same title already exists in the team.

Auth: LINEAR_API_KEY env var (personal key, sent verbatim — no `Bearer`).

Plan JSON schema (all keys optional except `updates[].match`):
{
  "project": "<project name>",
  "project_aims": "## Aims\n1. ...",            # appended to the project description iff it lacks "## Aims"
  "project_update": {"body": "...", "health": "onTrack|atRisk|offTrack"},
  "updates": [ { "match": {"kaibernetic": "<uuid>", "title": "..."},
                 "state": "In Review", "priority": 2,
                 "add_labels": ["needs-you"], "remove_labels": [],
                 "comment": "**Headline**\n..." } ],
  "new_issues": [ { "title": "...", "description": "...", "priority": 2, "state": "Todo",
                    "labels": ["needs-you"], "parent_match": {"title": "..."} } ]
}
"""
import argparse, json, os, sys, textwrap, urllib.request
from datetime import datetime, timezone

API = "https://api.linear.app/graphql"


def gql(query, variables=None, key=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "Authorization": key})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {json.dumps(out['errors'], indent=1)[:2000]}")
    return out["data"]


def age_days(iso):
    t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - t).total_seconds() / 86400


def freshness(days):
    return "green" if days <= 3 else ("yellow" if days <= 7 else "RED")


ISSUE_FIELDS = """
  id identifier title description priority updatedAt url
  state { id name } assignee { name } labels { nodes { id name } }
  parent { id identifier title } project { id name }
  comments(first: 50) { nodes { body createdAt } }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="ELE")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--assignee-me", action="store_true", help="assign created issues to viewer")
    a = ap.parse_args()
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:  # fallback: gitignored ~/Dev/pm-skills/.env with a LINEAR_API_KEY=... line
        envp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
        if os.path.exists(envp):
            for line in open(envp):
                if line.strip().startswith("LINEAR_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("error: LINEAR_API_KEY is not set (env var or ~/Dev/pm-skills/.env)")
    plan = json.load(open(a.plan))

    # ---- bootstrap -------------------------------------------------------------------------
    teams = gql("query { teams(first: 100) { nodes { id key name } } }", key=key)["teams"]["nodes"]
    team = next((t for t in teams if t["key"] == a.team), None) or sys.exit(f"team {a.team} not found")
    states = gql("query($id: String!) { team(id: $id) { states { nodes { id name type } } } }",
                 {"id": team["id"]}, key)["team"]["states"]["nodes"]
    state_id = {s["name"]: s["id"] for s in states}
    labels = gql("query { issueLabels(first: 250) { nodes { id name team { key } } } }", key=key)["issueLabels"]["nodes"]
    label_id = {}
    for l in labels:  # prefer workspace-level (team None), then this team
        if l["team"] is None or l["team"]["key"] == a.team:
            label_id.setdefault(l["name"], l["id"])
    viewer = gql("query { viewer { id name } }", key=key)["viewer"]

    proj_name = plan.get("project")
    projects = gql("query($n: String!) { projects(filter: { name: { eq: $n } }) { nodes { id name url description } } }",
                   {"n": proj_name}, key)["projects"]["nodes"]
    project = projects[0] if projects else sys.exit(f"project {proj_name!r} not found")

    issues = gql("query($pid: ID!) { issues(first: 200, filter: { project: { id: { eq: $pid } } }) { nodes {" + ISSUE_FIELDS + "} } }",
                 {"pid": project["id"]}, key)["issues"]["nodes"]
    team_issues = gql("query($tid: ID!) { issues(first: 250, filter: { team: { id: { eq: $tid } } }) { nodes { id identifier title state { name } project { name } } } }",
                      {"tid": team["id"]}, key)["issues"]["nodes"]

    # ---- orient() dashboard -----------------------------------------------------------------
    print(f"\n# {project['name']} — {project['url']}  ({len(issues)} issues; team {a.team} has {len(team_issues)})")
    has_aims = "## Aims" in (project["description"] or "")
    print(f"project description {'HAS' if has_aims else 'LACKS'} '## Aims' ({len(project['description'] or '')} chars)\n")

    def last_activity(i):
        ts = [i["updatedAt"]] + [c["createdAt"] for c in i["comments"]["nodes"]]
        return min(age_days(t) for t in ts)

    for i in sorted(issues, key=last_activity):
        d = last_activity(i)
        lab = ",".join(l["name"] for l in i["labels"]["nodes"])
        kb = "kaib" if "kaibernetic:" in (i["description"] or "") else "    "
        par = f" ⤷ {i['parent']['identifier']}" if i["parent"] else ""
        print(f"  {i['identifier']:<8} {i['state']['name']:<12} p{i['priority']} {freshness(d):<6} {d:5.1f}d  {kb}  {i['title'][:70]}{par}  [{lab}]  ({len(i['comments']['nodes'])} comments)")

    # ---- matching ----------------------------------------------------------------------------
    def match(m):
        kb = m.get("kaibernetic")
        if kb:
            for i in issues:
                if f"kaibernetic:{kb}" in (i["description"] or ""):
                    return i, "kaib"
        t = (m.get("title") or "").strip().lower()
        if t:
            for i in issues:
                if i["title"].strip().lower() == t:
                    return i, "title"
            for i in issues:
                if t in i["title"].strip().lower() or i["title"].strip().lower() in t:
                    return i, "substr"
            for i in team_issues:
                if i["title"].strip().lower() == t:
                    return i, "team-title(outside project)"
        return None, None

    actions = []  # (kind, payload, description)

    if plan.get("project_aims") and not has_aims:
        new_desc = (project["description"] or "").rstrip() + "\n\n" + plan["project_aims"]
        actions.append(("project_desc", {"id": project["id"], "description": new_desc},
                        f"PROJECT {project['name']}: append aims\n" + textwrap.indent(plan["project_aims"], "      ")))
    if plan.get("project_update"):
        pu = plan["project_update"]
        actions.append(("project_update", {"projectId": project["id"], "body": pu["body"], "health": pu.get("health", "onTrack")},
                        f"PROJECT UPDATE ({pu.get('health','onTrack')}):\n" + textwrap.indent(pu["body"], "      ")))

    print("\n## Plan matching")
    for u in plan.get("updates", []):
        iss, how = match(u["match"])
        label = u["match"].get("title") or u["match"].get("kaibernetic")
        if not iss:
            print(f"  ✗ UNMATCHED: {label!r}  (no write)")
            continue
        full = "comments" in iss
        print(f"  ✓ {iss['identifier']} [{how}] ← {label!r}" + ("" if full else "  (outside project: comment only)"))
        if not full:
            iss = gql("query($id: String!) { issue(id: $id) {" + ISSUE_FIELDS + "} }", {"id": iss["id"]}, key)["issue"]
        cur_state = iss["state"]["name"]
        if u.get("state") and u["state"] != cur_state:
            sid = state_id.get(u["state"]) or sys.exit(f"state {u['state']} missing on team")
            actions.append(("issue_update", {"id": iss["id"], "input": {"stateId": sid}}, f"{iss['identifier']}: state {cur_state} → {u['state']}"))
        if u.get("priority") is not None and u["priority"] != iss["priority"]:
            actions.append(("issue_update", {"id": iss["id"], "input": {"priority": u["priority"]}}, f"{iss['identifier']}: priority {iss['priority']} → {u['priority']}"))
        have = {l["name"] for l in iss["labels"]["nodes"]}
        for ln in u.get("add_labels", []):
            if ln not in have:
                actions.append(("add_label", {"id": iss["id"], "label": ln}, f"{iss['identifier']}: +label {ln}"))
        for ln in u.get("remove_labels", []):
            if ln in have:
                actions.append(("remove_label", {"id": iss["id"], "label": ln}, f"{iss['identifier']}: -label {ln}"))
        if u.get("comment"):
            head = u["comment"].strip().splitlines()[0].strip()
            dup = any(c["body"].strip().splitlines()[0].strip() == head for c in iss["comments"]["nodes"] if c["body"].strip())
            if dup:
                print(f"      (comment with headline {head!r} already present — skip)")
            else:
                actions.append(("comment", {"issueId": iss["id"], "body": u["comment"]},
                                f"{iss['identifier']}: COMMENT\n" + textwrap.indent(u["comment"], "      ")))

    existing_titles = {i["title"].strip().lower() for i in team_issues}
    for n in plan.get("new_issues", []):
        if n["title"].strip().lower() in existing_titles:
            print(f"  = exists, skip create: {n['title']!r}")
            continue
        parent = None
        if n.get("parent_match"):
            parent, how = match(n["parent_match"])
            if not parent:
                print(f"  ! parent not found for {n['title']!r} — will create without parent")
        inp = {"teamId": team["id"], "title": n["title"], "description": n.get("description", ""),
               "priority": n.get("priority", 3), "projectId": project["id"],
               "stateId": state_id.get(n.get("state", "Todo"), state_id.get("Todo"))}
        if parent:
            inp["parentId"] = parent["id"]
        if n.get("labels"):
            inp["labelIds"] = [label_id[l] for l in n["labels"] if l in label_id]
            missing = [l for l in n["labels"] if l not in label_id]
            if missing:
                print(f"  ! labels missing in workspace (create first): {missing}")
        if a.assignee_me:
            inp["assigneeId"] = viewer["id"]
        actions.append(("issue_create", {"input": inp},
                        f"CREATE [{n.get('state','Todo')} p{n.get('priority',3)}] {n['title']}" + (f"  ⤷ {parent['identifier']}" if parent else "") +
                        "\n" + textwrap.indent(n.get("description", ""), "      ")))

    print(f"\n## {'APPLYING' if a.apply else 'DRY RUN —'} {len(actions)} actions\n")
    for kind, payload, desc in actions:
        print("•", desc, "\n")
        if not a.apply:
            continue
        if kind == "issue_update":
            gql("mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success } }", payload, key)
        elif kind == "add_label":
            gql("mutation($id: String!, $l: String!) { issueAddLabel(id: $id, labelId: $l) { success } }", {"id": payload["id"], "l": label_id[payload["label"]]}, key)
        elif kind == "remove_label":
            gql("mutation($id: String!, $l: String!) { issueRemoveLabel(id: $id, labelId: $l) { success } }", {"id": payload["id"], "l": label_id[payload["label"]]}, key)
        elif kind == "comment":
            gql("mutation($input: CommentCreateInput!) { commentCreate(input: $input) { success } }", {"input": payload}, key)
        elif kind == "issue_create":
            r = gql("mutation($input: IssueCreateInput!) { issueCreate(input: $input) { issue { identifier url } } }", payload, key)
            print("   → created", r["issueCreate"]["issue"]["identifier"], r["issueCreate"]["issue"]["url"])
        elif kind == "project_desc":
            gql("mutation($id: String!, $input: ProjectUpdateInput!) { projectUpdate(id: $id, input: $input) { success } }",
                {"id": payload["id"], "input": {"description": payload["description"]}}, key)
        elif kind == "project_update":
            gql("mutation($input: ProjectUpdateCreateInput!) { projectUpdateCreate(input: $input) { success } }", {"input": payload}, key)
    if not a.apply:
        print("(dry run — re-run with --apply to write)")


if __name__ == "__main__":
    main()
