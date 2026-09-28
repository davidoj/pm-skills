# Backend adapter: Linear

Maps the operations vocabulary in `PRINCIPLES.md` to Linear. Each operation
lists the MCP path first (official Linear MCP server), then a GraphQL
fallback. Descriptive only — when/why to run operations is the skills' job.

## Access

| Path | Details |
|---|---|
| MCP (preferred) | `https://mcp.linear.app/mcp` (OAuth or API key; read-only variant at `/mcp/readonly`). Tool names **verified 2026-09-02** against the Claude Code Linear MCP: reads `list_issues`, `get_issue`, `list_projects`, `get_project`, `list_teams`, `get_team`, `list_issue_statuses`, `list_issue_labels`, `list_comments`, `get_user`; writes `save_issue` (create, or update when `id` is passed; supports `patch` for partial description edits), `save_project`, `save_comment`, `create_issue_label`. There are **no** `create_issue` / `update_issue` / `create_comment` tools — wherever those appear below, read `save_issue` / `save_comment`. |
| GraphQL (fallback) | `POST https://api.linear.app/graphql` with header `Authorization: <LINEAR_API_KEY>` — personal API keys take **no** `Bearer` prefix (only OAuth tokens use `Bearer <token>`). Body: `{"query": "...", "variables": {...}}`. Errors arrive in an `errors` array with HTTP 200 — always check it. |

**One-time bootstrap per team** (cache these IDs for the session):

```graphql
query { teams(first: 100) { nodes { id key name } } }          # pick team id
query States($teamId: String!) {
  team(id: $teamId) { states { nodes { id name type } } }      # workflow state ids
}
query { issueLabels(first: 250) { nodes { id name } } }        # label ids (workspace + team)
query { viewer { id name } }                                   # own user id, for claim()
```

## Fixed conventions

- **Canonical context doc** = the issue **description** (`revise_context` rewrites it).
- **Progress log** = issue **comments**, append-only (`append_progress` never edits old comments).
- **Initiatives** ↔ Linear **projects**. **Container tasks** ↔ parent issues (sub-issues via `parentId`).
- **Provenance** (migrated items): description ends with `---\nkaibernetic:<uuid> · migrated <date>` (migration script also appends ` · [original](<url>)`). Idempotency checks match on `kaibernetic:<uuid>`.
- **Agent-session staleness**: a `🤖 agent session started` comment older than ~4h with no subsequent activity on the issue is probably stale — treat the claim as released.

### State mapping (`set_state`)

| Source state | Linear |
|---|---|
| active / ready | Todo |
| in_progress | In Progress |
| blocked | Todo + label `blocked` + comment naming the blocker |
| paused | Backlog |
| completed | Done |
| archived / wont-do | Canceled |

State IDs come from the bootstrap `states` query (match by `name`); fall back to Todo (with a warning) if a name is missing on the team.

### Priority mapping

Linear scale: 0 = None, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low.

| Source priority | Linear priority |
|---|---|
| ≥ 2 | 1 (Urgent) |
| 1 | 2 (High) |
| 0 | 3 (Medium) |
| -1 | 4 (Low) |

### Freshness (for `orient()` rendering)

| Since last activity (`updatedAt` / latest comment) | Signal |
|---|---|
| ≤ 3 days | green |
| 3–7 days | yellow |
| > 7 days | red |

## Operations

### `orient()`

MCP: `list_issues` four times with the filters below, plus `list_projects`.
GraphQL: one aliased query.

Data pulls: (1) issues labeled `needs-you`; (2) In Progress issues by
`updatedAt` desc; (3) Todo issues with priority Urgent/High; (4) Done in the
last 14 days; (5) active projects.

```graphql
query Orient($teamId: ID!) {
  needsYou: issues(first: 20, filter: {
    team: { id: { eq: $teamId } }, labels: { name: { eq: "needs-you" } } })
    { nodes { identifier title updatedAt url } }
  inFlight: issues(first: 50, orderBy: updatedAt, filter: {
    team: { id: { eq: $teamId } }, state: { name: { eq: "In Progress" } } })
    { nodes { identifier title updatedAt assignee { name } url } }
  ready: issues(first: 20, filter: {
    team: { id: { eq: $teamId } }, state: { name: { eq: "Todo" } },
    priority: { lte: 2, neq: 0 } })    # 0 = No priority; 1–2 = Urgent/High
    { nodes { identifier title priority url } }
  recentDone: issues(first: 10, filter: {
    team: { id: { eq: $teamId } }, completedAt: { gt: "-P2W" } })
    { nodes { identifier title completedAt } }
  projects(first: 50, filter: { state: { eq: "started" } })  # VERIFY: legacy string field; newer schemas use status { type }
    { nodes { id name state targetDate } }
}
```

Date comparators accept ISO-8601 relative durations (`"-P2W"` = two weeks ago).

### `load(task)`

MCP: `get_issue(id)` (+ `list_comments` if comments aren't inlined `# VERIFY`).
GraphQL:

```graphql
query Load($id: String!) {
  issue(id: $id) {
    id identifier title description url priority updatedAt
    state { name type } assignee { name } labels { nodes { name } }
    project { id name } parent { identifier title }
    children(first: 50) { nodes { identifier title state { name } } }
    relations(first: 50) { nodes { type relatedIssue { identifier title } } }
    comments(first: 100) { nodes { body createdAt user { name } } }
  }
}
```

Purpose/definition-of-done live in the description (canonical doc); history is
the comment stream, oldest→newest.

### `claim(task)` / `release(task)`

Claim = assignee → the user, state → In Progress, plus a session comment.

- MCP: `save_issue(id, assignee="me", state="In Progress")`, then
  `save_comment(issueId, "🤖 agent session started: <session-id>")`.
  Linear also has a native `delegate` field for *registered* Linear agents;
  Claude Code is not one, so the session comment remains the agent-working
  signal. Assignee = human owner; delegate/comment = agent at the keyboard.
- GraphQL:

```graphql
mutation Claim($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) { success }
}
# variables: { "id": "<issue>", "input": { "assigneeId": "<viewer.id>", "stateId": "<In Progress id>" } }

mutation($input: CommentCreateInput!) { commentCreate(input: $input) { success } }
# body: "🤖 agent session started: <session-id>"
```

Release = comment `🤖 agent session released` (same `commentCreate` / `create_comment`).
State **stays** In Progress — releasing signals "no one at the keyboard", not "work stopped".

### `append_progress(task, note)`

- MCP: `save_comment(issueId, note)`.
- GraphQL: `commentCreate` as above. Append-only: never edit or delete prior comments.

### `revise_context(task, doc)`

- MCP: `save_issue(id, description=doc)` — or `save_issue(id, patch=[...])` for surgical edits that keep the rest (preferred for appending).
  Gotcha: Linear **normalizes stored markdown** (bare URLs become `[host](<url>)` links, `-` bullets become `*`), so `patch` anchors must match the *stored* text — re-read with `get_issue` before anchoring on anything you wrote earlier. A failed patch saves nothing, including any label changes in the same call.
- GraphQL: `issueUpdate(id, input: { description: $doc })`.

This **overwrites** the whole description — read it first, and preserve the
`kaibernetic:<uuid>` provenance footer if present.

### `flag_user(task, ask)` / `clear_flag(task)`

Flag = add label `needs-you` + comment starting `**Needs you:** <ask>`.
Clear = remove the label (optionally comment the resolution).

- MCP: `save_issue(id, addLabels=["needs-you"])` + `save_comment`; clear with
  `save_issue(id, removeLabels=["needs-you"])`. Verified: `labels=` **replaces** the
  whole set; `addLabels` / `removeLabels` merge — use those.
- GraphQL (safe path — `labelIds` replaces the full set, so read-modify-write):

```graphql
query { issue(id: "<id>") { labels { nodes { id } } } }
mutation { issueUpdate(id: "<id>", input: { labelIds: [<current ids>, "<needs-you id>"] }) { success } }
mutation($input: CommentCreateInput!) { commentCreate(input: $input) { success } }  # "**Needs you:** <ask>"
```

Direct single-label mutations `issueAddLabel(id, labelId)` /
`issueRemoveLabel(id, labelId)` also exist and avoid the read step.

Create the label once if missing (MCP: `create_issue_label(name)` — omit `teamId` for a workspace-level label; check whether `needs-you` already exists in your workspace first):

```graphql
mutation { issueLabelCreate(input: { name: "needs-you", teamId: "<team>" }) { issueLabel { id } } }
```

### `create(item)`

Task → issue; initiative → project. Description starts with the purpose line;
home = `projectId` (initiative) and/or `parentId` (container task).

- MCP: `save_issue(team, title, description, priority, state, project, parentId, labels, assignee="me")`;
  projects via `save_project(name, addTeams=[...], lead="me", state, summary, description)` (verified).
- GraphQL:

```graphql
mutation($input: IssueCreateInput!) {
  issueCreate(input: $input) { issue { id identifier url } }
}
# input: { "teamId": ..., "title": ..., "description": ..., "priority": 2,
#          "stateId": ..., "projectId": ..., "parentId": ..., "labelIds": [...] }

mutation($input: ProjectCreateInput!) {
  projectCreate(input: $input) { project { id name url } }
}
# input: { "name": ..., "description": ..., "teamIds": ["<team>"] }
```

### `complete(task, reason)`

Set state Done + a closing comment whose reason **names follow-ups** (create
follow-up issues first, then reference their identifiers in the comment).

- MCP: `save_issue(id, state="Done")` + `save_comment(issueId, "Done: <reason>. Follow-ups: ENG-124, ENG-125")`.
- GraphQL: `issueUpdate(id, input: { stateId: <Done id> })` + `commentCreate`.

### `set_state(task, state)`

Apply the state-mapping table via `save_issue(id, state=...)` /
`issueUpdate(id, input: { stateId: ... })`. For **blocked** additionally add
the `blocked` label and post a comment naming the blocker (issue identifier or
external cause). When unblocking, remove the label.
