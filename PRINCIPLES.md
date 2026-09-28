# Principles

Why this repo exists, what "working well" means, and the shared vocabulary the
skills are written in. Every skill here is an application of this page.

## The problem

Serious work now happens across many short-lived, parallel AI-agent sessions.
The failure mode isn't amnesia — plenty persists between sessions: the repo,
the transcripts, memory files, the tracker itself. It's that what persists is
rarely saved with strategy or maintained afterwards. Records land in whatever
shape the moment produced, go stale silently, and a stale claim reads exactly
like a fresh one — an unmaintained record is worse than a blank slate,
because it still looks like memory. So work done in session N misleads
session N+1, parallel sessions collide or duplicate, and obligations
mentioned once in passing evaporate. A tracker is the shared memory that
makes sessions composable — but only if the way agents *use* it preserves a
few invariants.

These skills encode those invariants. They are deliberately about **results,
not steps**: they tell you what must be true when you're done, and trust you
to get there sensibly in context. When a skill and your judgment conflict on
*how*, follow your judgment; when they conflict on *whether the invariant
holds*, the invariant wins.

## The desiderata

Everything below is in service of these. When improvising in a situation the
skills don't cover, optimize for these directly.

1. **Truthful State.** Recorded statuses match reality closely enough to be
   trusted. A dashboard that lies is worse than none — it manufactures false
   confidence. Done means verified done; in-progress means someone is actually
   progressing it; blocked names the blocker.
2. **Attention Routing.** The system surfaces what deserves attention now,
   rather than making the user triage everything. A good check-in is a small,
   credible set of next actions — not a wall of fifty items.
3. **Spin-off Closure.** Obligations discovered mid-work reliably come back
   into attention later. Spin-offs are where progress leaks out of a system:
   "we should also fix X" said once and never seen again. Capture must be
   cheap, and captured things must resurface.
4. **Flow Continuity.** A session can end abruptly and the next one resumes
   without the user reconstructing their mental model. The trail — not the
   user's memory — carries the context.
5. **Forward Momentum.** Every report-back names the next concrete step, or
   explicitly confirms the goal is reached. The journey never just hangs.
6. **Delegation Readiness.** Tasks are recorded well enough that someone else
   (human or agent) could pick them up: the why, the definition of done, and
   the current state are on the task, not in anyone's head.

## Design principles

- **Specify results, not steps.** Define what must be true; let the agent
  figure out how. Checklists rot; invariants don't.
- **Describe vs prescribe.** Tool and API docs *describe* (neutral contracts).
  Skills *prescribe* (opinionated ways of working) — and may be freely edited,
  because they live with the user, not the vendor.
- **Minimal overhead on the hot path.** Structure belongs at boundaries
  (pickup, meaningful milestones, close) — not on every message. If hygiene
  is slowing the work, you're doing too much of it, too often.
- **The agent does the micro-hygiene.** Statuses, notes, links, flags are the
  agent's job. The user contributes only what the agent can't know: intent,
  priorities, decisions.

## The operations vocabulary

Skills are written against these abstract operations. The mapping to a
concrete backend (Kaibernetic, Linear, ...) lives in `backends/` — read
`backends/ACTIVE.md` first to find which adapter is live.

| Operation | Meaning |
|---|---|
| `orient()` | Fetch attention data: user-flagged items, in-flight work + last activity, ready high-priority items, recent completions, active initiatives/projects |
| `load(task)` | Full context: purpose, definition of done, canonical context doc, progress history, relationships |
| `claim(task)` / `release(task)` | Signal active work started / stopped, so parallel sessions don't collide |
| `append_progress(task, note)` | Append to the task's history. Never rewrites history |
| `revise_context(task, doc)` | Deliberate rewrite of the canonical context doc (rare; confirm first) |
| `flag_user(task, ask)` / `clear_flag(task)` | Route a specific ask to the user's attention / resolve it |
| `create(item)` | New task/initiative with a purpose line, a home, a priority |
| `complete(task, reason)` | Mark done; the close reason names follow-ups |
| `set_state(task, state)` | Blocked / paused / ready / etc. |

Two distinctions the vocabulary bakes in, because losing them causes real
failures:

- **Canonical doc vs history.** Every task has one editable statement of
  where things stand (`revise_context`) and an append-only trail of how it
  got there (`append_progress`). Rewriting history destroys the audit trail;
  letting the canonical doc rot buries the current state under archaeology.
- **Flagging vs releasing.** Stopping work (`release`) and needing the user
  (`flag_user`) are different acts. A task that's waiting on a human decision
  but only "released" disappears from everyone's attention — the single most
  common way work silently dies.
