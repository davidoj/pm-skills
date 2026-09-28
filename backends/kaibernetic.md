# Backend adapter: Kaibernetic (MCP)

Maps the operations vocabulary in `PRINCIPLES.md` to the Kaibernetic MCP
tools. This doc is descriptive — semantics and gotchas of the tools, not
advice on when to use them (that's the skills' job).

| Operation | Tool call |
|---|---|
| `orient()` | `check_in(mode="auto")` — server-assembled dashboard (see notes) |
| `load(task)` | `get_context(item_id)` — accepts UUID (reliable) or fuzzy title |
| `claim(task)` | `get_context(item_id, claim=True)` at pickup, or `save_progress(ongoing_claim=True, ...)` while working |
| `release(task)` | `save_progress(suspend=True, mark_complete=False, ...)` |
| `append_progress(task, note)` | `save_progress(mark_complete=False, ongoing_claim=..., ...)` — structured fields below |
| `revise_context(task, doc)` | `update_goal(item_id, context_md=..., nuke_context=True)` — **overwrites**; quote and confirm first |
| `flag_user(task, ask)` | `save_progress(needs_user="<ask>")` — implicitly releases the claim |
| `clear_flag(task)` | `save_progress(clear_needs_user=True, ...)` |
| `create(item)` | `add_goal(content, description, context_md, parent_title, contributes_to, theory_of_impact, ...)` |
| `complete(task, reason)` | `save_progress(mark_complete=True, ...)`; set `close_reason` via `update_goal` when follow-ups need naming |
| `set_state(task, state)` | `update_goal(item_id, status=...)` — active / in_progress / blocked / paused / completed / archived |
| ad-hoc analytics | `query_database(sql)` — SELECT freely; UPDATE only on goals/contributions, auto-snapshotted, `RESTORE <batch_id>` to undo |

## Semantics worth knowing

- **Two kinds of claim.** `claimed_by` (person-level ownership, via
  `update_goal(claim_user=True)`) vs `agent_session` (ephemeral "someone is
  working right now", via the claim/release calls above). Agent sessions
  older than ~4h are presumed stale; a warning on claim is soft — claiming
  proceeds.
- **`save_progress` is append-only** and never touches `context_md`. It
  requires an explicit completion decision (`mark_complete`) and, when not
  completing, an explicit claim decision (`ongoing_claim` true/false or
  `suspend`). Structured fields: `current_focus`, `progress_notes`,
  `realizations`, `micro_tasks`, `direction_change`, `detailed_notes`,
  `active_files`, `user_contributions`.
- **`needs_user` carry-forward.** An outstanding ask is carried forward
  automatically on later `save_progress` calls; it clears only via
  `clear_needs_user=True`. `needs_user` cannot combine with
  `ongoing_claim=True` or `mark_complete=True`.
- **`add_goal` validates purpose.** Non-initiative items must ladder to an
  initiative via `contributes_to`, and every link needs a specific
  `theory_of_impact` — creation is rejected otherwise. Single
  `blocks`/`improves`/`affects` link auto-parents the item there.
  `description` = 1–2 lines for lists; `context_md` = the full doc.
- **`list_goals(goal_title=<uuid>)`** scopes the tree to one project; default
  output is minimal (titles+status), `include_details=True` for more.
- **Dashboard internals** (if reproducing `orient()` via `query_database`):
  needs-you = latest progress update carrying a `needs_user` ask (cap 20);
  in-flight = `status='in_progress'` by last progress desc (cap 50);
  ready = `status='active'` with an initiative ancestor, not blocked, by
  priority (cap 20); completed = last 14 days (cap 10); initiatives =
  kind in (initiative, milestone), focused first. Freshness: green ≤3d,
  yellow 3–7d, red >7d since last activity.
