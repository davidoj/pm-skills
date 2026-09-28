---
name: pm-close
description: Close out a work session — reconcile statuses with reality, flag what needs the user, name the next step. Use when ending or handing off a session, before context runs out, or when the user says "wrap up".
---

# pm-close — leave the system truthful

**Serves:** Truthful State, Forward Momentum, Spin-off Closure, Flow
Continuity (`PRINCIPLES.md`).

## Why this moment matters

The close is the exit surface — the last moment this session's knowledge can
be written down by the one party who has it. It's also where the tracker's
credibility is won or lost: every claim left stale, every "done" that isn't,
every ask left unflagged degrades the next check-in for everything else.

## The result you're producing

When the session ends, all of these hold:

1. **Statuses match reality.** Finished work is marked done — with a close
   reason that names any follow-ups it spawned. Unfinished work is *not*
   marked done, however close it feels; "done" is a verified claim, not a
   forecast. Discrepancies you noticed (merged PRs, resolved blockers) are
   reconciled, not left for the next reader to trip on.
2. **The trail supports resumption.** The final progress entry says where
   things stand, what's verified vs assumed, and what the immediate next
   move is (see `pm-log`). Your session's claim is released so the task
   reads as available, not as phantom live work.
3. **Asks are flagged as asks.** If the next step belongs to the user —
   merge, review, decision, credential, smoke test — flag it with the
   specific ask (`flag_user`), don't just release. A bare release is only
   right when another agent could pick the task straight up from the trail.
   This distinction is the single biggest determinant of whether work
   resurfaces or silently dies.
4. **Spin-offs are landed.** Everything discovered-but-not-done this session
   is captured, deferred, or dropped per `pm-capture` — nothing lives only
   in the conversation.
5. **The parent knows, if it needs to.** If this work completed a piece of
   something larger, revealed a blocker, changed scope or direction — put a
   line where the containing work's readers will see it. If the work turned
   out to matter for a reason the project's stated aims don't cover, add that
   aim to the project — aims are what keep purpose lines referential (see
   `pm-capture`). If none of those happened, don't touch the parent.
6. **The report-back names the next step.** End with either the next
   concrete action (and whose it is) or explicit confirmation that the goal
   is reached. "Review my changes", "I'll continue with X next session",
   "this is done, verified by Y" all qualify. A summary that just trails
   off does not.

7. **The read on screen is fresh.** If `~/.config/pm/hud.json` exists, run
   `pm-orient` as the very last step. A close changes the board — flags
   raised, items done, spin-offs filed — and the HUD keeps showing the
   pre-close read until something re-reads the tracker. Only a full read
   earns a new `generated_at` (see `pm-hud`); patching the items you touched
   would leave a file that looks fresh and is half stale. The orient read
   also doubles as the check that the board now tells the truth.

## Judgment guidance

- Close-time is also gap-review time: if a question you hit mid-session
  reveals a systematic gap (task context that should have existed, a policy
  that's missing), say so now — cheaply fixing the system beats silently
  absorbing its defects. If the gap is in the PM system's own spec —
  conventions, adapter, a skill's prescription — revise it via `pm-tune`.
- Scale ceremony to the session. A two-message Q&A session needs none of
  this; a session that touched tracked work needs all of it. When in doubt,
  the test is: *would the next session be worse off if this weren't
  written?*
- The report-back, and any description you rewrite, follow the house style
  (`~/Dev/pm-skills/STYLE.md`): summary first, details after, plain
  sentences.

- **If the close includes a commit, assume the checkout is shared.** Several
  sessions often work in one working tree, so `git status` mixes their work.
  Stage by explicit path (`git add <files you changed>`), never `git add -A`,
  `git add .` or `git commit -a`; check `git diff -- <file>` holds only your
  hunks; name the files in the message; leave other sessions' modified files
  alone and say what you left; post the commit hash in the trail so other
  sessions know HEAD moved. A commit that sweeps another session's half-edited
  file is a wrong statement with a real hash (2026-09-16,
  reward_hacking_geometry `98129b1`, fixed forward in `1ce2d08`).

## Backend

Read `~/Dev/pm-skills/backends/ACTIVE.md`, then the active adapter:
`append_progress`, `release` / `flag_user`, `complete`, `create` for
spin-offs.
