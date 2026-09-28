---
name: pm-pickup
description: Start work on a tracked task — load its context, claim it, sanity-check the scope. Use when beginning substantive work in a session, before writing code or making changes.
---

# pm-pickup — start work without going in blind

**Serves:** Flow Continuity, Truthful State, Delegation Readiness
(`PRINCIPLES.md`).

## Why this moment matters

The pickup is where continuity is either inherited or lost. Prior sessions
left a trail — plans, half-done work, dead ends already explored — and the
cheapest mistake to avoid is re-deriving or contradicting it. It's also where
parallel-session collisions are prevented, and the last cheap moment to catch
a mis-scoped task before effort is sunk into the wrong thing.

## The result you're producing

Before you change anything, all of these hold:

1. **You can state the task's why, its definition of done, and what's already
   been tried.** If you can't, you haven't loaded enough — read the task's
   canonical doc, its history, and any inherited context/policies from its
   parents. Exploration to *scope* the work is always fine before this;
   *implementation* isn't.
2. **The work is signaled.** The task is claimed (`claim`) so other sessions
   see live work. If someone else's claim looks active — recent, not
   hours-stale — surface it instead of silently working in parallel.
3. **The right task exists.** Match the session's actual purpose to a
   specific task. If the closest match is a generic container ("Backend
   API"), create a specific child for this work (see `pm-capture`) — history
   logged against containers is history nobody finds. If you resolved the
   task by fuzzy name, verify the match before trusting it.
4. **Scope gaps are triaged, not swallowed.** If the task context doesn't
   answer a question you need: make a sensible call and note it in the
   trail when it's cheap to reverse; stop and flag the user when the
   options serve different ultimate purposes and the right choice isn't
   apparent, when reversing would be expensive, or when the gap looks like
   one that will recur. Don't interrupt for calls you'd normally make
   yourself — the close-session review is the safety net for those.

## Judgment guidance

- Prefer stable IDs over title matching when both are available; duplicated
  titles land fuzzy matches on the wrong task.
- Inherited context flows downward: a parent's policies (testing
  requirements, deployment gates, conventions) bind the child. Check them at
  pickup, not at review time.
- If the trail contradicts reality (task says blocked but the blocker
  shipped), reconcile the record first — you're the freshest eyes on it.

- **On a shared checkout, `git status` mixes several sessions' work.** Treat
  modified files you did not touch as another session's in-progress edits: do
  not revert, reformat or commit them. Re-read a file immediately before
  editing it, since it may have been rewritten since you last read it, and
  prefer anchored replacements to whole-file writes.

## Backend

Read `~/Dev/pm-skills/backends/ACTIVE.md`, then the active adapter:
`load(task)` and `claim(task)`.
