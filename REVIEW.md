# Review guide — what moved, what changed, what got dropped

Generated 2026-08-24 for the initial extraction. The **Judgment calls** section
is the review target: those are opinions, not translations. The traceability
table below it is for spot-checking fidelity.

## Judgment calls to check

1. **Theory of Impact was softened from enforced ceremony to a judgment bar.**
   Kaibernetic's `add_goal` *rejects* creation without a TOI and the old
   guidance mandated asking the user for one. `pm-capture` keeps the essence —
   a purpose line + "if we shipped this and nothing improved, what did we
   misjudge?" — but nothing enforces it. On Linear there is no server-side
   validation at all, so capture discipline rests entirely on the skill.
   *This is the experiment's central bet: do unenforced results contracts
   hold up?*
2. **The 7-step Standard Procedure was dissolved, not ported.** Its content
   survives as result contracts spread across pickup/log/close, but there is
   no longer a numbered mandatory sequence or Pre-Work Checklist gate. If you
   believe the *gate* (MUST NOT write code before task load) did real work,
   that teeth is gone.
3. **The Policy-Gap Protocol was compressed to two sentences** (pm-pickup #4:
   raise-vs-proceed calibration; pm-close: gap-review at exit). The 3-way
   triage taxonomy (wrong readiness call / task context gap / missing global
   policy) and the paired-upstream-fix rule were dropped as too
   Kaibernetic-process-specific.
4. **The hierarchy taxonomy (Project → Business Domain → Functional Area →
   Task) was not ported.** Skills only say "give work a home near related
   context." Structure conventions are left to each backend's adapter. Same
   for contribution types (blocks/improves/measures/tests/discovered_from) —
   only "record the blocking relationship" survives generically.
5. **Initiative laddering is no longer required.** Old rule: every task must
   ladder to an initiative or be dropped. New rule: every item needs a
   purpose line. Weaker on portfolio coherence, cheaper on ceremony.
6. **Container-goal protection, task granularity ("don't atomize"), the
   6–12-month deferral test, and needs-user-vs-suspend** all survived intact —
   the last one promoted to a first-class principle (flagging vs releasing).
7. **check_in's mechanics moved to the adapter; its editorial judgment became
   the skill.** pm-orient carries compress-green/expand-red, summary-line
   first, reconcile-against-repo-reality, end-with-recommendation. Thresholds
   (3/7d) live in adapters. If pm-orient reads thin to you, that's where to
   push.
8. **Scale-of-ceremony escape hatch added** (pm-close: "a two-message Q&A
   session needs none of this"). The old guidance had no explicit opt-down;
   this risks under-logging if the judgment is miscalibrated.

## Traceability: old guidance → new home

| Source guidance | New home | Notes |
|---|---|---|
| Pre-Work Checklist (list_goals → task → get_context) | pm-pickup contract 1–3 | Gate → contract (see call #2) |
| Standard Procedure steps 1–2 (load task, establish plan) | pm-pickup | |
| Steps 3–5 (narrate, log often, record spin-offs) | pm-log, pm-capture | |
| Step 6 (close the loop) | pm-close 1–2 | |
| Step 7 (Forward Momentum: name next step) | pm-close 6 | Verbatim in spirit |
| save_progress norms (append-only; headline; action/result/implication; artifacts; user contributions separate) | pm-log 1–4 | |
| needs_user vs suspend | pm-close 3 + PRINCIPLES "flagging vs releasing" | Promoted |
| needs_user carry-forward semantics | backends/kaibernetic.md | Backend mechanics |
| Spin-off protocol (when to spin off; blockers get tasks + relationship) | pm-capture; pm-log judgment | |
| Task granularity (checklist vs N siblings) | pm-capture judgment | Intact |
| Containers are scaffolding; never complete from a subtask | pm-capture judgment | Intact |
| Timeliness assessment (6–12mo tooling test) | pm-capture state 2 (deferred) | Intact |
| Theory of Impact (mandatory, strong-vs-weak) | pm-capture state 1 | Softened (call #1) |
| Initiative laddering requirement | pm-capture "purpose line" | Weakened (call #5) |
| Contribution types decision tree | — (adapter territory) | Dropped (call #4) |
| Hierarchy taxonomy | — (adapter territory) | Dropped (call #4) |
| Policy-Gap Protocol | pm-pickup 4; pm-close judgment | Compressed (call #3) |
| Context Loading Protocol (pull_parent_context policies) | pm-pickup judgment ("inherited context flows downward") | Mechanism dropped, principle kept |
| Parent Update Triggers (5 triggers) | pm-close 5 | "New subtask needed" trigger folded into pm-capture |
| Context quality (why/what/how; err verbose; description vs context_md) | pm-log; pm-capture 1; kaibernetic.md | Split |
| check_in dashboard mechanics (sections, caps, 3/7d, modes) | backends/*.md orient() recipes | |
| check_in presentation judgment | pm-orient | See call #7 |
| Agent claim vs person claim; 4h staleness | backends/kaibernetic.md; linear.md conventions | |
| Clickable task links | backends/ACTIVE.md | |
| UUIDs over fuzzy titles; verify matches | pm-pickup judgment | |
| update_goal destructive / confirm rewrites | PRINCIPLES (canonical doc vs history) + kaibernetic.md | |
| "MUST follow, non-negotiable" framing | — | Replaced by PRINCIPLES: invariants win, methods don't |

## Not ported (out of scope for this pass, by agreed scope)

- weekly-review, staleness sweep, hierarchy health, librarian skills;
  close-session *eval* (the observational desiderata scoring — still lives in
  FlowDnA `.claude/skills/close-session`); focus-slot management;
  query_database analytics recipes beyond orient().

## Second pass (same day): setup/draft_plan content ported after all

David correctly pushed back that the new-project addendum, plan-drafting
guidance, and capability-horizons reference are standalone content — the
"entangled with onboarding PR" caveat applies to changing the *server tools*,
not to porting their content here. Ported as three skills with a different
translation policy than the work-loop five:

- **Near-verbatim, thin fronts.** `pm-init/elicitation.md` and
  `pm-plan/drafting.md` are the eval-tuned production prompts (v3* lineage) —
  NOT rewritten into results-contract style, because the prose is the tuned
  artifact. SKILL.md fronts add the results framing; the reference files are
  the skill. Edit them with care, ideally re-eval.
- **Adaptations made:** the two tool hand-offs re-pointed (`draft_plan` →
  pm-plan, `horizons()` → pm-horizons); backend vocabulary mapped via a note
  in pm-plan (context_md / global_context / show_recent_work); the
  Kaibernetic-product "Post-Plan Onboarding" section (MCP setup instructions)
  dropped.
- **Judgment call #9 — horizons provenance flagged.** `pm-horizons` warns
  that the condensed task list is a production derivative (only partly
  traceable to David's hand-rated predictions) and that the frontier table
  is a Feb 2026 baseline (~one doubling stale by late 2026); it points to
  `tasks_round2_annotated.md` + `/horizons-checkin` as canonical. If you'd
  rather the skill embed the canonical 131-task set directly, say so.

## Review outcomes (David, 2026-09-02)

- **Call #1 (Theory of Impact softened): accepted.** The purpose line stays a judgment bar, now made *referential* — it cites the containing project's numbered Aims, and an unlisted reason becomes a new aim on the project (pm-capture, pm-close).
- **Call #2 (Standard Procedure dissolved): accepted, conditional on agents invoking the skills at the right moments.** The trigger surface is each skill's frontmatter `description` ("Use when …"), which every Claude Code session loads into its skill list, plus the boundary list in the FlowDnA `CLAUDE.md` work-tracking section. This is a soft trigger (model judgment), not the hard gate the Pre-Work Checklist was. The dogfood week + the close-session eval are the check. Fallback if triggers prove unreliable: Claude Code hooks (SessionStart → `pm-orient`; PreToolUse on Edit/Write → `pm-pickup` reminder).
- **Call #3 (Policy-Gap Protocol compressed): accepted with a tightening.** "When it's about direction" was too vague; pm-pickup #4 now reads "when the options serve different ultimate purposes and the right choice isn't apparent" (plus expensive-to-reverse and likely-to-recur).
- **Single-sourcing decision:** the "Why this moment matters" sections stay — a line-by-line check showed five of six carry moment-specific reasons and behavioural steers ("err verbose", "last cheap moment to catch mis-scoping", "an unflagged ask degrades the next check-in") that exist nowhere else. `PRINCIPLES.md` was previously cited but never read; `backends/ACTIVE.md` (the file every skill reads first) now instructs reading it once per session. pm-capture's Why, the one true duplicate of desideratum 3, was de-duplicated.
- **Calls #4–#9: accepted as written** ("otherwise looks good", same session).
