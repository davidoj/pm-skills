---
name: pm-capture
description: Capture new work — tasks, spin-offs, follow-ups, blockers — so it resurfaces at the right time. Use whenever new obligations emerge, mid-work or in conversation ("we should also...", "file that for later").
---

# pm-capture — things said once must resurface

**Serves:** Spin-off Closure, Attention Routing, Delegation Readiness
(`PRINCIPLES.md`).

## Why this moment matters

Spin-off Closure (desideratum 3) is decided here, not at close. Mid-work
you'll uncover follow-ups, adjacent bugs, hardening ideas, blockers — each
obvious in the moment, each gone by next session unless it lands somewhere
that resurfaces it, in a form that survives a future reader who lacks
today's context.

## The result you're producing

Every new obligation ends the session in exactly one of these states:

1. **Captured with a purpose.** The item exists in the tracker with: a title
   a stranger can parse; a *why* line that **cites which of the containing
   project's stated aims it advances** (projects list their aims — reference
   the aim, don't paraphrase a private version of it) and what you'd
   conclude if you shipped it and nothing improved (if you can't answer
   that, you haven't understood the item yet — ask). If it matters for a
   reason the project's aims don't state, that's a finding, not a gap to
   paper over: add the aim to the project, or flag it. Then: enough context
   that pickup doesn't require re-discovery (see `pm-pickup`'s bar: why,
   done-means, current state); a home near related work, because related
   context is the main thing a home provides; and an **owner** (assignee) —
   even solo, even when obvious, because unowned items route to nobody.
2. **Explicitly deferred.** Real, but not now — parked with a reason and,
   ideally, a revisit condition. One worth asking about non-trivial items:
   *will 6–12 months of tooling progress make this dramatically easier?*
   If yes and it's not urgent, deferring is the strong move.
3. **Explicitly dropped.** "Not important" is a fine answer — but say it and
   drop it. The silent middle state, mentioned-but-never-recorded, is the
   failure this skill exists to prevent.

If the new work blocks the current task, also record that relationship and
stop working the blocked side (see `pm-log`).

## Judgment guidance

- **Search before you create.** Query the tracker for the title's key terms
  first; a duplicate is the cheapest structural rot to prevent and the most
  expensive to merge later.
- **Right-size the structure.** N related small pieces serving one goal =
  one task with a checklist. A separate task is earned by a distinct
  definition of done, a different owner, or a real handoff. Over-atomizing
  scatters context; under-atomizing hides work.
- **Containers are scaffolding.** Don't log work against broad areas or
  initiatives — create the specific task. And don't mark containers complete
  because one child finished.
- **Priority is a claim, not a vibe.** High priority should be justifiable
  in a sentence; when everything is high, nothing is routed.
- **Write it to the house style.** `~/Dev/pm-skills/STYLE.md`: a plain
  summary first, the done-means checklist, then an appendix for paths, ids,
  numbers, and quotes. Provenance goes in the appendix, not the purpose line.

## Backend

Read `~/Dev/pm-skills/backends/ACTIVE.md`, then the active adapter:
`create(item)`; `set_state` for deferrals; relationships per adapter.
