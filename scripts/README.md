# scripts

## migrate_kaibernetic_to_linear.py

Migrates an exported active slice of a Kaibernetic goal tree into Linear (projects + issues).

1. **Export** — the agent produces `data/export.json` via Kaibernetic MCP `query_database` (SELECT the active slice, shape rows to the schema below).
2. **Expected JSON** — `{"exported_at": "<ISO>", "items": [{kaibernetic_id, title, kind: task|initiative|milestone|area, status: in_progress|active|blocked|paused, priority, parent_title, initiative, description, context_md, recent_progress: [str], needs_user, url}]}`.
3. **Dry-run (default)** — `LINEAR_API_KEY=lin_api_... python scripts/migrate_kaibernetic_to_linear.py --team ENG` prints the full plan (key needed for read-only skip detection).
4. **Apply** — add `--apply`. Idempotent: re-runs skip issues whose description carries `kaibernetic:<uuid>`; projects are matched by name.

Mappings (states, priorities, labels `migrated`/`needs-you`/`blocked`) follow `backends/linear.md`.

## linear_apply_plan.py

Applies a reconciliation plan (JSON: project aims/update, per-issue state/label/comment updates,
new issues) to a Linear project. **Dry-run by default**: prints an `orient()` dashboard of the
project's live issues (state, freshness, labels), matches each plan entry by `kaibernetic:<uuid>`
footer → exact title → substring, and prints every write it would make. `--apply` writes;
`--assignee-me` assigns created issues to the viewer. Comments are idempotent on their headline;
issue creation is skipped when the title already exists in the team.

```bash
python3 my_plan.py > plan.json                                                   # your plan generator → JSON (keep it outside the repo; data/ is gitignored)
LINEAR_API_KEY=lin_api_... python3 scripts/linear_apply_plan.py --team <KEY> --plan plan.json
python3 scripts/linear_apply_plan.py --team <KEY> --plan plan.json --apply --assignee-me
```

The key may also live in the gitignored `.env` (`LINEAR_API_KEY=...`).

