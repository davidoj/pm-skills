---
name: close-session
description: "End-of-session close, orient, then evaluation. Runs pm-close (reconcile statuses, flag asks, land spin-offs), then pm-orient (a fresh read that also refreshes the pinned HUD), then evaluates the workflow desiderata (Truthful State, Attention Routing, Spin-off Closure, Delegation Readiness, Flow Continuity, Right-Sized Structure, Forward Momentum, Strategic Embedding) against the post-close state. Compact mode does only the persist step, before context compaction. Triggers: /close-session, close session, session eval, end session, /close-session compact, save progress before compacting. Ask for it explicitly before compaction, before quitting, or when handing off; the model cannot start it on its own."
---

# close-session — close, orient, then evaluate

**Serves:** every desideratum, at the session boundary (`PRINCIPLES.md`). The
close is where this session's knowledge is written down by the one party who
has it; the orient read is the user's re-entry point; the eval is the
calibration instrument that tells us whether the skills are working.

Everything written here, progress entries, comments, the report, follows
`STYLE.md` at the repo root.

## Usage

```
/close-session            → pm-close + pm-orient + eval
/close-session compact    → persist only, before context compaction (no orient, no eval)
/close-session eval       → eval only (the close already ran or was not needed)
```

## Compact mode

Context is about to compact, but the session continues. Do the persist step
and nothing else; the full close comes later.

1. **Identify the touched tasks.** If none were loaded, say so and skip to 3.
2. **Log per `pm-log`.** One entry per touched task: headline, then what was
   done, decisions, findings, files and commits, and the immediate next move.
   Leave the session claim in place; work is continuing.
3. **Memory candidates.** Anything from the session that belongs in the
   file-based memory (feedback, project facts, references) is saved now.
4. **Breadcrumb.** End with a short block so the post-compaction context does
   not start cold: task title and link, one line of status, one to three
   bullets of what comes next. This is not the close summary.

---

## Phase 1: Close

Run `pm-close` against the active backend (`backends/ACTIVE.md`). When it is
done:

- Statuses match reality (done is verified done; unfinished is not done)
- The trail supports resumption (final progress entry per touched issue;
  session claim released)
- Asks are flagged as asks (`flag_user` with the specific ask), not merely
  released
- Spin-offs are captured, deferred, or dropped; nothing lives only in the
  conversation
- The report-back names the next step and whose it is

**Do this first, fully, before Phase 2.** The eval assesses the *result* of
the close, not the process. The close should behave identically whether or
not the eval will run afterward.

---

## Phase 2: Orient

Run `pm-orient`. Two reasons, both cheap at a boundary:

- It is the user's re-entry point, so it has to be right *after* this
  session's changes. If the pinned HUD file exists, this is what refreshes it
  (pm-close's result 7). Patching the HUD by hand is not a substitute: only a
  full read earns a new `generated_at`.
- Its output is the evidence for Phase 3: what the board actually says now,
  not what this session believes it wrote.

Keep the orient output in hand for the eval.

---

## Phase 3: Evaluate

**Goal:** assess whether the workflow desiderata are satisfied in the
post-close state. This is observational: it checks what is true, it does not
fix anything.

### 1. Identify session scope

Scan the conversation to determine:

- Which tracked issues were touched (loaded, created, progressed, rewritten,
  in the operations vocabulary of `PRINCIPLES.md`)
- What work was done (code changes, investigations, decisions, discussions)
- What new tasks or spin-offs were created
- Whether any follow-up work was identified, persisted or not
- Session type: well-scoped autonomous task, draft-and-refine, exploratory
  discussion, mixed or crystallizing, or stewardship or portfolio

### 2. Pull in updates from other sessions

Other sessions may have updated touched tasks while this one ran. That work
must be incorporated before you evaluate or decide anything.

**Get the session start timestamp.** Claude Code transcripts live at
`~/.claude/projects/<project-slug>/<session-id>.jsonl`; the first line's
`timestamp` is the session start. Use this session's own id, which the
harness exposes in the scratchpad path. Do not assume the most recently
modified transcript is this session: with parallel sessions it often belongs
to a sibling.

```bash
python3 -c "
import json, sys
p = sys.argv[1]   # this session's transcript path
with open(p) as f:
    for line in f:
        if line.strip():
            o = json.loads(line)
            if o.get('timestamp'): print(o['timestamp']); break
" ~/.claude/projects/<project-slug>/<session-id>.jsonl
```

**Query for updates since then.** For each touched issue, list its comments
newest first and keep those created after the session start that this
session did not write. Parallel sessions post under the same user, so tell
them apart by content and timing; a `🤖 agent session started` line names
the session. Also compare each touched issue's current state, assignee, and
labels with what this session last set. Any such change is cross-session
activity to incorporate before evaluating. If another session closed a task,
do not re-flag it; if it added a progress note with new information, factor
that into Truthful State and Flow Continuity.

### 3. Use the Phase 2 orient read as the reference

The orient read is the user's primary re-entry point and the HUD's source.
Verify assessments against it, not only against issue descriptions: an
issue's context may be thorough, but if the orient read does not surface it
or misrepresents it, the user will not see it.

### 4. Evaluate the desiderata

For each, assess **pass / warn / fail** with a brief note.

**Rate the state at the moment the eval starts, not after in-eval
corrections.** If you notice a gap during the eval and fix it (a missing
flag, a stale claim, a missing definition of done), the rating stays warn or
fail. Note the fix in Items to Address with the prefix `[fixed in-eval]` and
record it in the JSONL field `in_eval_fixes`. Silently upgrading ratings
after fixes makes the log look cleaner than reality and hides recurring
patterns. `pass` is reserved for states that were already correct when the
eval began.

#### 4a. Truthful State

> Recorded statuses match reality closely enough to be trusted.

For each task touched this session:

- **Status accuracy.** Completed work marked complete; blocked work marked
  blocked or flagged; in-progress work with its session claim handled, not
  dangling; work not started still unstarted.
- **Sub-agent task completion.** Tasks worked by background agents need
  explicit resolution: done, flagged with the specific user action, or left
  in progress with a clear note on what is next. A task released with no
  flag and no pickup mechanism will not re-enter anyone's workflow.
- **Progress recency.** The latest entry reflects what actually happened:
  decisions, investigation results, blockers.
- **Cross-session visibility.** Another session picking up any touched task
  would know where it is up to from the record alone.
- **Orient-read accuracy.** For each touched issue, quote what the orient
  read shows and say whether it gives the user a correct impression.

Pass: all touched issues accurate, recent, correct in the orient read,
sub-agent tasks resolved. Warn: minor gaps. Fail: a wrong status, unsaved
progress, a misleading orient line, or a dangling sub-agent task.

#### 4b. Attention Routing

> The system surfaces what deserves attention now instead of making the user
> search for it.

Looking at the orient output: completed work from this session appears in
the finished section; every needed user action appears in the needs-you
section; the user could tell what to do next without opening tasks; this
session's outputs are findable, not buried.

Pass: a clear, correct picture of what needs the user and what is next.
Warn: the information is in the system but not prominent (in flight without
a flag despite needing the user). Fail: needed user actions not surfaced, or
completed work missing.

#### 4c. Spin-off Closure

> Follow-up tasks created during work reliably come back into attention.

For each task created this session: could a cold-start agent make progress
within two minutes from its record; is it linked to a parent or project that
brings it back; does it have an owner; are blocking relations set. Also:
were follow-ups, open questions, or TODOs mentioned in conversation and not
captured?

Pass: all spin-offs well-contexted and routed, no uncaptured follow-ups.
Warn: thin context, or some follow-ups uncaptured. Fail: important follow-up
work discussed and not captured, or spin-offs floating unconnected.

#### 4d. Delegation Readiness

> Tasks are delegatable at the right level.

For each task touched this session, the five highest-leverage checks:

1. **A definition of done exists.** Missing it degrades everything else.
2. **Ownership is assigned and serviceable.** An agent-only claim with no
   pickup workflow is false confidence.
3. **Scope is clear.** Explicit in and out for features; clear boundaries
   for tasks.
4. **The verification surface covers the risk.** "Tests pass" is not enough
   if the work touches deployment config, environment variables, or
   third-party integrations.
5. **Inherited policies are referenced.** If a parent carries testing or
   deployment requirements, the definition of done points at them;
   delegatees tunnel on the checklist in front of them.

Pass: all touched issues have a definition of done, serviceable ownership,
clear scope, adequate verification. Warn: minor gaps. Fail: no definition of
done, no owner, or scope a delegatee would struggle with.

#### 4e. Flow Continuity

> A session can pause and resume without the user reconstructing their
> mental model.

Resumability for agents (the canonical doc plus the latest entry tell the
whole story); resumability for the user (after a night's sleep they would
know what happened and what needs them); low-ceremony capture (the agent
maintained the trail without being driven); a clear "what changed, new
state, what needs you" somewhere persistent.

Pass: re-orientation in under two minutes from stored state alone. Warn:
some decisions or results only in the transcript. Fail: significant work in
no persistent artifact.

#### 4f. Right-Sized Structure

> No more structure than the work requires.

Per `pm-capture`'s right-size guidance: independent parallel work belongs in
one task with a checklist; a sibling earns its own row only with a distinct
definition of done, a different owner, or a real handoff.

For each spin-off: did it need its own row; should siblings under one parent
have been one task with a checklist; is nesting depth proportional to scope;
did containers accumulate micro-progress that belongs on a leaf.

Pass: appropriate granularity throughout. Warn: borderline cases. Fail:
parallel items split into siblings that one checklist would have served, or
micro-progress on a container.

#### 4g. Forward Momentum

> Every user-facing report named the next step, or confirmed done.

Did each meaningful report-back end with a named next step or an explicit
done; were there silent stalls where the user had to ask "what next?"; does
the close output make next moves explicit, with asks spelled out rather
than "blocked".

Pass: every report-back named a next step or confirmed done, close output
explicit. Warn: a few trailed off. Fail: repeated stalls or an ambiguous
close.

#### 4h. Strategic Embedding

> New tasks are connected to why they matter.

Spin-off Closure checks that new tasks come back into attention; this checks
that they are connected to the goals they serve. The mechanism depends on
the backend: in Linear it is project membership, the parent issue, and the
purpose line citing the project's aim numbers with a null-result sentence
(`pm-capture`); in Kaibernetic it was contribution links each carrying a
theory of impact. Contribution is transitive, so coverage is checked by
reachability through the parent and project chain, not by direct links to
everything.

For each task created this session:

- **Coverage.** Every project or aim the work materially advances is
  reachable through the task's chain. If not, repair the chain at the
  ancestor when the contribution conceptually flows through it (that fixes
  all siblings), or add a direct cross-link with its own rationale when the
  task advances the goal by a mechanism the chain does not describe.
- **Considered, not structural.** The home was chosen because the work
  advances that goal, not because the tool required a parent.
- **Specific rationale.** The purpose line says what changes if this ships
  and what that moves forward. "Implements parent functionality" fails.
- **Falsifiable.** "If we ship this and the goal does not improve, what was
  our wrong assumption?" is answerable from the record.

Pass: every relevant goal reachable, sparse considered links, specific
falsifiable rationale. Warn: a thin rationale or an unexamined borderline
goal. Fail: placeholder rationale, a home chosen for tool acceptance, or a
clearly relevant goal unreachable and untriaged. N/A if no tasks were
created.

### 4.5. Detect contextual workflow patterns

Scan the needs-you items and the touched issues for three recurring
patterns. Each produces a pasteable call to action in Items to Address. The
four shapes of a needs-you ask are pure-user, agent-preppable, agent-only,
and dangling-session.

**Pattern 1, manual test (agent-preppable).** Trigger: an ask whose text
reads "verify", "click", "open the page", "check that X appears", or
similar. Such asks are often mislabelled pure-user when an agent could drive
the click-through, set up state, and leave only the visual judgment to the
user. Template:

> **[Agent-preppable] [Task title]:** the user-facing part of this ask is the
> visual or judgment OK. Spin up an agent session: *"Pick up `<KEY-N>`. Run
> the manual checks in the needs-you ask: drive the UI, verify each element,
> set up state. When it is ready for visual review, flag the user with the
> original ask plus 'ready for visual OK, see screenshots' and stop."* Then
> the user does the visual OK only.

**Pattern 2, stale needs-you (barrier review).** Trigger: a flag set more
than seven days ago and still outstanding. Something is making it hard to
close; the barrier may itself be a task. Template:

> **[Stale needs-you, barrier review] [Task title]:** flagged since `<date>`.
> What is blocking? If the barrier is setup or infrastructure (a test user,
> a staging environment), spin it off as its own task with a definition of
> done; otherwise re-flag with a more concrete ask, or decide it is not
> critical and clear it.

**Pattern 3, parent blocked by an unstarted child (kick-off).** Trigger: a
parent whose own work is complete but which cannot close because a child is
still unstarted. The block is agent-doable; surface the kick-off, not the
wait. Template:

> **[Parent blocked by child] [Parent title]:** parent otherwise complete;
> held open by `<child KEY-N> <child title>`. Kick off an agent session on
> the child: *"Pick up `<child>`. Context: `<two lines>`. Complete per its
> definition of done; the parent can then close."*

Detection: match needs-you text against Pattern 1's phrases; compute days
since flagged from the flag comment's timestamp for Pattern 2; walk children
and check status for Pattern 3. These are suggestions the eval does not act
on.

### 4.6. Settle issue closure explicitly

The user should never have to ask "so did anything actually get closed?".
Before writing the report, put every task touched or created into exactly
one bucket:

- **Closed this session.** Its definition of done is met and you set the
  status. Say which criterion each one satisfied.
- **Closeable but not yours to close.** The definition of done looks met but
  the judgment belongs to the user (a review verdict, a subjective call,
  work another session owns). Name it, say what remains, leave the status.
- **Still open.** Say the one thing it is waiting on.

Report "none" out loud: a session that closed nothing is normal, but it must
be stated. Do not close on partial evidence; a wrongly closed task stops
resurfacing. Also sweep for issues nominally open but stale, In Progress or
In Review for more than a few days or flagged needs-you, and pair each with
what would unblock it.

### 5. Produce the report

```
## Session Eval Report

**Agent / model:** [e.g. claude-code / fable-5-1]
**Session type:** [well-scoped / draft-and-refine / exploratory / mixed / stewardship]
**Tasks touched:** [list with links]
**Tasks created:** [list with links, or "none"]
**Tasks closed:** [list with links, or an explicit "none"]
**Tasks still open:** [every task touched or created that is not closed: id, status, the one thing it waits on]

### Desiderata

Ratings reflect the state at eval start, before any in-eval corrections.

| Desideratum | Rating | Notes |
|---|---|---|
| Truthful State | ✅/⚠️/❌ | |
| Attention Routing | ✅/⚠️/❌ | |
| Spin-off Closure | ✅/⚠️/❌ | |
| Delegation Readiness | ✅/⚠️/❌ | |
| Flow Continuity | ✅/⚠️/❌ | |
| Right-Sized Structure | ✅/⚠️/❌ | |
| Forward Momentum | ✅/⚠️/❌ | |
| Strategic Embedding | ✅/⚠️/❌ | |

### In-Eval Fixes

[Anything the eval itself corrected, each naming the desideratum it would
have downgraded. Empty if none.]

### Items to Address

[Open items after the eval, including in-eval fixes that need follow-up and
suggestions the eval did not act on.]

### Observations

[Patterns noticed; workflow quality this session.]
```

### 6. Persist the eval

Append one JSONL line to `.claude/logs/close-session-evals.jsonl` in the
working project's repo, creating the directory and file if needed:

```json
{
  "timestamp": "2026-04-20T06:15:00Z",
  "session_id": "<session id>",
  "session_start": "<first transcript timestamp>",
  "session_type": "mixed",
  "agent": "claude-code",
  "model": "fable-5-1",
  "tasks_touched": ["KEY-1", "KEY-2"],
  "tasks_created": ["KEY-3"],
  "tasks_closed": [],
  "ratings": {
    "truthful_state": "warn", "attention_routing": "warn",
    "spin_off_closure": "warn", "delegation_readiness": "warn",
    "flow_continuity": "fail", "right_sized_structure": "pass",
    "forward_momentum": "pass", "strategic_embedding": "pass"
  },
  "items_to_address": ["short description"],
  "in_eval_fixes": ["[truthful_state] set needs-you on task X, was released without an ask"],
  "observations": ["pattern 1"],
  "cross_session_activity": [{"goal_id": "KEY-1", "session_id": "other", "note": "..."}]
}
```

Ratings are `pass`, `warn`, `fail`, or `na`. `agent` and `model` are
required when known. `in_eval_fixes` is what keeps the ratings honest:
ratings reflect the pre-fix state, this field captures the cleanup.

Then post a one-line pointer to the entry on the tracker's eval-log home,
the issue named as `eval_home` in `backends/ACTIVE.md`, so the
slow-iteration loop stays visible in the live tracker. The pointer names the
session, the ratings that were not pass and why, the log line, and any
observation that bears on the skills themselves.

---

## Edge cases

- **No tracked issues loaded.** Still run the eval; check whether tasks
  should have been created. The no-task case is itself a finding.
- **Exploratory or discussion session.** Truthful State and Delegation
  Readiness may be N/A; Flow Continuity and Spin-off Closure still apply
  (was the outcome captured?).
- **Several tasks touched.** Evaluate each; the report rolls up.
- **Very short session, under five exchanges.** Skip the full eval; "nothing
  substantive to evaluate" is fine.
- **Eval-only mode.** For checking state without running the close, or
  auditing mid-session.

## Backend

Read `backends/ACTIVE.md` for the active adapter and for `eval_home`. The
operations used here are `pm-close`'s, `pm-orient`'s, and `append_progress`
for the eval pointer.
