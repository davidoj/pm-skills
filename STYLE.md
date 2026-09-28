# Style — how tracker text reads

Applies to everything a skill writes for a person to read: issue titles and
descriptions, comments and log entries, project docs, plan summaries, the
orient read, the close report. The content rules in the skills say what a
record must contain. This page says how it reads. Where the two seem to pull
apart, the resolution is always the same: the summary stays short because it
is read, the appendix stays complete because it is searched.

**Serves:** Attention Routing and Delegation Readiness (`PRINCIPLES.md`). A
record nobody can read routes no attention and delegates nothing.

**Sources merged here.** The content requirements from `pm-capture`, `pm-log`
and `pm-pickup`. The readability rules Claude Code's harness applies to
messages for the user. The shape from Open Philanthropy's reasoning
transparency guidance (Muehlhauser, 2017): open with a summary of the key
conclusions, link the details, then give the details. Trigger: a 2026-09-16
review of a research project's board found the issues effortful to read. Each
rule that produced them was sound on its own. Together they put the whole
evidence base in the first paragraph.

## The shape: summary, done-means, appendix

A reader who stops after the summary has a true picture. A reader picking the
task up goes to the appendix. Every description has these three parts in this
order.

1. **Summary.** Three to eight sentences of plain prose. What this is. Which
   project aim it serves, by number. What we will know when it is done. What
   we would conclude if we shipped it and nothing improved. Current state in
   one sentence if the task is live. Confidence where it matters. It ends by
   naming what the appendix holds.
2. **Done means.** The checklist. Linear renders `- [ ]` items, so keep them,
   one line each. An item may point at an appendix section by name.
3. **Appendix.** Everything else: paths, flags, commands, queue ids,
   versions, numbers with their sources, verbatim quotes, design tables,
   caveats. Messy is fine. Sectioned with short headings so the summary can
   point at a section by name, as in "see Appendix: runs".

Two invariants tie the layers together. The summary does not carry what the
appendix exists for. The appendix does not introduce a claim the summary
lacks: it holds the evidence and detail behind the summary's claims, not a
second copy of them. Provenance stays mandatory, which prompt, which
checkpoint, which pool, which commit, but it lives in the appendix.

Log entries and comments have the same shape at smaller scale: a headline
line, then action, result, and implication in up to three sentences, then
links, then an appendix if there is one.

## Sentence rules

These are the harness rules for messages to the user, applied to the summary
and to log headlines. The appendix may use tables and terse notation.

- **Lead with the outcome.** If something could not be verified, say so
  first.
- **One idea per sentence,** about twenty words, with a verb. A sentence beats
  a label with a colon. Start a new sentence instead of joining clauses with a
  semicolon.
- **No em-dashes, no parentheticals, no arrows** in the summary.
- **Code out of prose.** Name a file, function, flag, or run id only when the
  reader has to go there. At most one per sentence and two per paragraph in
  the summary. Describe the rest in words or move it to the appendix.
- **Numbers out of prose.** A number appears in the summary only if it
  changes what the reader does, and then on its own line or in a short table.
  Every rate in the appendix names its prompt and its checkpoint.
- **Expand an uncommon acronym on first use.** Define a term of art in a
  clause on first use.
- **Say who said what.** "David decided X on 2026-09-15", not "per
  discussion". Paraphrase in the summary. Quote verbatim in the appendix when
  the wording matters.
- **Refer to other issues by title plus key,** as links, never by UUID. Say
  what the other issue is, not just its number.
- **Bullets for parallel items,** one or two sentences each. Bold the first
  few words of a bullet, never a whole sentence. No headers inside a summary.
  Headers in the appendix are welcome.
- **Stop when the content stops.** No closing offer, no restating.

## Titles

Object plus operation, under about eighty characters. No question, no
colon-then-explainer, no dash-separated subtitle. The question goes in the
summary's first sentence.

Too much: *add_goal latency: parent picker on a 1200-goal account (cold cache)
vs the bulk-ancestry path — is the round-trip count the 15 s culprit?*

Enough: *add_goal latency: parent picker on a 1200-goal account*

## What stays from the content rules

Nothing here relaxes a content requirement. It only decides where each thing
lives.

- **Purpose cites the project aim by number** (`pm-capture`). Summary.
- **The null-result sentence,** what you would conclude if it shipped and
  nothing improved (`pm-capture`). Summary.
- **Why, done-means, current state, what was tried** (`pm-pickup`'s bar).
  Summary and done-means; the detail of what was tried goes in the appendix.
- **Action, result, implication; turning points marked; the user's
  contributions credited separately** (`pm-log`). Headline and first lines of
  a log entry.
- **Err verbose in the trail** (`pm-log`). Resolved: verbosity is about the
  appendix being complete, not about the headline being dense.
- **Plans keep `drafting.md`'s section format** (`pm-plan`). It is
  eval-tuned. These rules govern the sentences inside it.
- **Descriptions a colleague could skim** (`backends/ACTIVE.md`). This page
  is what that means.

## Jargon and private names

Agents coin names. A session calls something "the picker path", "arm
B", "the roster page", or `focus_vacate_v2`, and the next reader, human or
agent, meets the name with no way to decode it. Project terms of art have the
same problem one step removed: "slot", "roster", "vacated" mean
something exact to the people who set them and nothing to anyone else. Two of
the rules below borrow defect names from David's writing-loop defect library
(local, not part of this repo).

- **Every term of art and every invented name is defined somewhere the
  reader can reach from the text.** A term the summary leans on gets a clause
  on first use: "the roster, the list of up to three initiatives a user has
  marked as current focus". The rest go in an appendix section called Terms,
  and the summary says it is there. Terms is for what a colleague outside the
  project would not know, not a glossary of every noun in the text. A term
  used as if already introduced but never introduced is a defect: an orphan
  reference.
- **Do not coin a name when one exists.** Before naming something, check
  what the project already calls it: the project doc, WORKFLOWS.md, earlier
  issues. When a new name is needed, say so the first time, "call this the
  matched-rate test", and put it in Terms. Prefer a descriptive name to a
  cute one. A run id or experiment tag is a pointer, not a name. The words
  for it come first and the id follows, in the appendix.
- **No private-context framing.** Phrasing that only earns its keep for
  someone who was in the room: "application (b) of the Track 3 list", "the
  lever the margin panel only simulates". The test: what in this text makes
  this the natural way to say it? If nothing does, give the referent in the
  text or drop the phrase.
- **Recurring terms may be defined once and linked.** If a term is already
  defined in a project doc or an earlier issue, link there from Terms rather
  than redefining it. The link is the definition's address. A bare "as
  usual" or "the standard recipe" is not.

## Self-check before saving

1. Can a colleague say what the task is for after the first two sentences?
2. Is any summary sentence over thirty words? Any em-dash, arrow, or
   parenthetical in it?
3. More than one identifier in a sentence, or two in a paragraph, of the
   summary?
4. Is there a number in the summary prose that does not change what the
   reader does?
5. Does every summary claim have its evidence in the appendix?
6. Is every appendix section named, so the summary can point at it?
7. Is every term of art and every invented name defined in a clause, under
   Appendix: terms, or by a link to where it was defined?
8. Is there a phrase that only makes sense to someone who was in the
   conversation?

## Worked example

A Kaibernetic issue from July 2026, "add_goal parent-picker latency", as first
written carried the whole evidence base in one paragraph: every measurement,
every function name, nested issue links, and quoted fragments of the user. Its
first sentence was a bold label wrapping a link, a dated quote, and an arrow.

The same issue in this style opens:

> Creating a goal through the MCP server takes 11 to 19 seconds on the largest
> account, past the 15-second timeout most MCP clients apply, so the call fails
> for exactly the users with the most data. The time is not the network: the
> parent picker makes one round trip per candidate parent, about eighty on a
> 1200-goal account, to build breadcrumbs it could fetch in one query.
>
> It serves aim 2, a hosted service people can rely on, and answers whether the
> latency is a round-trip problem or a cross-region one. If one bulk ancestry
> fetch brings the call under two seconds, round trips were the cause and the
> region can stay. If it does not, rate of round trips is not the input and the
> region moves.
>
> State on 2026-07-21: the bulk fetch is implemented behind a flag and measured
> at six round trips against a production-scale local copy. Terms, the harness,
> the measurements and caveats are in the appendix.

The measurements, the identifiers, and the quotes all survive. They sit in
appendix sections named Terms, Measurements, Harness, Caveats, and the user's
words, and the done-means items point at them by name. Terms defines the
parent picker, breadcrumbs, round trip, the bulk ancestry fetch and the client
timeout, so "the picker path" stops being a private name.
