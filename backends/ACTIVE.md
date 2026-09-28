# Active backend

**Read once per session, before the first skill runs:** `../PRINCIPLES.md`
(~800 words) — the desiderata every skill's *Serves* line refers to. Skills
carry the moment-specific why; the system-level why lives only there, so
updating a principle updates every skill.

**Backend:** `linear` — see `backends/linear.md`. `backends/kaibernetic.md` is
the adapter for the retired Kaibernetic backend and stays as a reference
implementation.

## Workspace specifics

Anything that identifies a particular workspace (its URL, teams, your user,
the `eval_home` issue, board scope) lives in `backends/ACTIVE.local.md`, which
is gitignored and machine-local. **If that file exists next to this one, read
it too.** If it does not, `pm-setup` creates it from the template below after a
live read of the backend.

### Conventions that hold for any Linear workspace
- Auth: the Linear MCP server (OAuth) in Claude Code, configured at **user
  scope** so it exists from any directory (project-local scope only shows up in
  that one repo). If a session has no `linear-server` tools:
  `claude mcp add --transport http --scope user linear-server https://mcp.linear.app/mcp`,
  then `/mcp` once to authenticate. `LINEAR_API_KEY` only for the GraphQL
  fallback and the scripts (key from env or the gitignored `.env`; see
  `scripts/README.md`).
- `assignee: "me"` works in `save_issue`.
- Labels: `needs-you` (= `flag_user`). Create `blocked` on first use; both are
  workspace-level.
- Workflow states (Linear defaults): Backlog, Todo, In Progress, In Review,
  Done, Canceled, Duplicate.
- Projects carry a numbered `## Aims` list in their description; issue purpose
  lines cite aim numbers (see `pm-capture`).
- `eval_home`: the issue where `close-session` posts its one-line eval pointer;
  the JSONL record itself lives in the working project's
  `.claude/logs/close-session-evals.jsonl`.
- Task links: `[Title](https://linear.app/<workspace>/issue/<KEY-N>)`. Refer to
  issues by title (+ key), not UUID.
- In a shared workspace, scope `orient()` and the HUD to issues assigned to you
  (`assignee: "me"`); do not report colleagues' issues as stale or change their
  state.

### Template for `ACTIVE.local.md`

```markdown
# Workspace specifics (machine-local, gitignored)
- Workspace: <name> — https://linear.app/<workspace-slug>.
- Teams: <KEY> ("<name>") — <what it holds>; <KEY> ("<name>") — <what it holds>.
- User: <email>.
- eval_home: <KEY-N> — <title>.
- Board scope: <e.g. only issues assigned to me>.
- Labels present: needs-you, <others>.
- Notes: <anything a fresh session needs to know about this workspace>.
```