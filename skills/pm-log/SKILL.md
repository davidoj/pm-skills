---
name: pm-log
description: Log work progress so any future session can resume it. Use at meaningful boundaries during work — a result landed, a decision made, a blocker hit, a direction changed.
---

# pm-log — make the work resumable

**Serves:** Flow Continuity, Truthful State, Delegation Readiness
(`PRINCIPLES.md`).

## Why this moment matters

The trail is the product, almost as much as the work itself. Sessions end
abruptly — context fills, users step away, machines sleep. Whatever isn't in
the trail when that happens is gone, and the next session pays for it in
rediscovery. Tokens are cheaper than rediscovery; err verbose.

## The result you're producing

A stranger — human or agent, next week — could pick up where you stopped
using nothing but the task's record. Concretely:

1. **The trail is append-only.** Progress goes on as history
   (`append_progress`), never by rewriting what's there. Rewrite the
   canonical doc (`revise_context`) only for deliberate re-statements of
   where things stand, and confirm before overwriting.
2. **Each entry carries action → result → implication.** Not "worked on
   auth" but "tried X, got Y, which means Z next." A headline first, so the
   entry is skimmable. Link the artifacts — commits, PRs, files, run logs —
   because links are how a future reader gets from claim to evidence.
3. **Turning points are marked.** Decisions, dead ends ("tried A, doesn't
   work because B" saves the next session from trying A), realizations, and
   direction changes — with what triggered them. These entries pay for
   themselves more than routine status does.
4. **The user's contributions are credited separately.** Decisions,
   insights, and work the user did are recorded as theirs — the record
   should distinguish what the human decided from what the agent inferred,
   or accountability blurs.

## Judgment guidance

- **Log at boundaries, not on a timer.** A result landed, a decision made, a
  blocker hit, scope shifted — those are entries. Play-by-play narration is
  noise that buries the signal. If nothing a future session would need has
  happened, there's nothing to log yet.
- **Blocked is a state, not a note.** If work can't proceed, set the state,
  name the blocker (as its own task if it needs doing — see `pm-capture`),
  and stop pushing on the blocked path.
- **Entries read to the house style.** `~/Dev/pm-skills/STYLE.md`: a headline
  line, then action, result, and implication in plain sentences; paths, ids,
  and numbers below that. "Err verbose" is about the appendix being complete,
  not the headline being dense.

## Backend

Read `~/Dev/pm-skills/backends/ACTIVE.md`, then the active adapter:
`append_progress(task, note)`, `revise_context` for deliberate rewrites,
`set_state` for blocked/paused.
