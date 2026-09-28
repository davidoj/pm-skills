---
name: pm-horizons
description: AI capability-horizon reference for planning — where the autonomous frontier is by domain, and the automate/defer/invest decision framework. Use during plan drafting for per-step horizon calls, ambition calibration, or "should we do this now or wait for better tooling" decisions.
---

# pm-horizons — plan against a moving frontier

**Serves:** Forward Momentum via ambition calibration; the timeliness test
in `pm-capture` ("will 6–12 months of tooling progress make this trivial?")
is this skill applied at capture time.

## What's here

[`reference.md`](reference.md) carries:
- The **frontier table** by domain (SWE, writing, data, ops, design, sales,
  strategy, robotics) with doubling rates.
- The **reference task set** (~50 condensed entries, `aggressive –
  conservative` horizon estimates).
- The **4-question decision framework** per plan step: where is the task
  vs the horizon → automate now / human review / human-led; when does the
  horizon arrive → defer or invest minimally; durable asset vs automatable
  work; cost of waiting.
- **AI-aware vertical integration**: route around AI-hard steps by
  restructuring the workflow so AI-cheap capabilities substitute for them.

## Calibration warnings — read before leaning on numbers

1. **Staleness.** The frontier table is a **February 2026** baseline with a
   ~4–6.5-month doubling rate — by late 2026 assume roughly one doubling of
   drift. Treat "now" entries as safely now, and shift boundary cases one
   bucket toward feasible. Recheck against current evidence before making a
   load-bearing call.
2. **Provenance.** The condensed task list is a production derivative:
   only part of it traces directly to David's hand-rated predictions
   (SWE and Data entries are faithful; some other domains were re-authored
   or back-filled during adaptation). The canonical source is the 131-task
   rated set at
   `kaibernetic/analysis/capability_horizon_eval/tasks_round2_annotated.md`
   (FlowDnA repo), updated monthly via `/horizons-checkin`. For any
   decision that actually hinges on a horizon value, prefer the canonical
   set — or better, its latest Resolution Log entries.
3. **Uncertainty discipline.** High-confidence verdicts ("definitely
   viable"/"definitely not") are usually unavailable; give calibrated reads
   with concrete reasoning, and treat the user as a co-judge, not an
   audience.
