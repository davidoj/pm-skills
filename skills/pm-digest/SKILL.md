---
name: pm-digest
description: Personal variant of the team daily-digest skill. It uses pm-orient's needs-you, going-stale and moving sections, and adds due soon and ready. Syncs yesterday's checked-off daily-note todos back to Linear, then sorts the user's Linear work into due soon, needs you, going stale, moving and ready, and shows new inbox email and Discord DM notifications. Asks which todos to focus on and writes them as a checklist into today's daily note. Use when the user runs /pm-digest or asks for the pm digest.
---

# pm-digest

**Serves:** Attention Routing, Truthful State, Forward Momentum (`PRINCIPLES.md`).

This is a personal copy of the `daily-digest` skill from `~/agent-setup`. It needs `~/agent-setup` and its settings, so it is not part of the portable pm-skills set. Step 2 is different: it lists only the user's own Linear issues. It uses pm-orient's needs-you, going-stale and moving sections and freshness limits, and adds due soon and ready. The other steps match `daily-digest`, and they use the same settings and state file.

Run the steps in order. Keep the output short and easy to scan, because the user reads it first thing in the morning. **Only make the changes listed in steps 1, 6 and 7, and the session rename in Setup.** Don't mark emails as read, reply to anything, or change Linear in any other way.

## Setup

- **Settings:** read the `## Daily digest settings` section of `~/.agents/personal.md`. If the section or a setting is missing, stop. Name the missing setting and point the user to `~/agent-setup/personal.md.example`.
- **Tools:** this skill needs the Linear MCP server (`~/agent-setup/docs/linear.md`), the Gmail connector (`~/agent-setup/docs/google.md`) and a folder of daily notes (`~/agent-setup/docs/obsidian.md`). If one is missing, say which, skip the steps that need it, and continue.
- **Today's date:** run `TZ=<time zone> date +%F`, with the time zone from the settings. The machine may run on UTC.
- **Session name:** rename this Claude Code session to `PM digest YYYY-MM-DD` (today's date), so you can tell the sessions apart. Use the session-management tools: call `get_session` with no arguments to get the session ID, then call `set_session_title`. If those tools are not available, skip this step and say so in one line.
- **Daily notes:** `<daily notes folder>/YYYY-MM-DD.md`. Edit the files directly.
- **Linear:** the team and projects from the settings. Done status: `Done`.
- **State file:** `~/.local/state/daily-digest/last-run` holds the date of the previous digest (`YYYY-MM-DD`). It may not exist yet.

In the steps below, `<KEY>` is the Linear team key and `<workspace URL>` is the Linear workspace URL from the settings.

## 1. Sync the previous daily note back to Linear

1. Find the most recent daily note **before today**. List the daily notes folder, sort the `YYYY-MM-DD.md` names, and take the newest one earlier than today. It might not be yesterday's.
2. Find every checked item (`- [x]` or `- [X]`, at any indent) that contains a Linear ID matching `\b<KEY>-\d+\b`.
3. Look up each of those issues. If it isn't already `Done` or `Canceled`, set its state to `Done` with `save_issue`. Don't change anything else on it.
4. Checked items **without** an ID: if one clearly matches an open Linear issue's title, list the match and **ask** before marking it done. Never mark it automatically.
5. Report this as one short line, such as "Marked done in Linear from 2026-11-07: ENG-56, ENG-57". Say so if nothing needed syncing.

## 2. Linear work

Sort the user's Linear work by what it needs from them, not by project. Only show issues that are assigned to the user.

**Get the issues.** Call `list_issues` in the team with `assignee: "me"`. Request these fields: `title`, `status`, `statusType`, `project`, `priority`, `dueDate`, `updatedAt`, `parentId`, `createdBy`, `createdById`, `createdAt`, `assigneeId`, `labels`, `description` and `url`. Follow `cursor` while `hasNextPage` is true.

1. Open issues: call it once each with `state: "backlog"`, `"unstarted"` and `"started"`.
2. Done issues: call it with `completedAt: "-P14D"`.

To get the latest comment on an issue in Needs you or Going stale, call `list_comments` with `orderBy: "createdAt"`. Show the comment with the latest `createdAt`, and skip inline comments on the description (`quotedText` is set).

**Sections.** Put each open issue in the first section that it fits, so it appears only once. If an issue in Due soon also belongs in Needs you, show its ask and latest comment too.

1. **⏰ Due soon:** overdue or due in the next 7 days, from any project, sorted by due date. Give the days left in words ("**OVERDUE by 2 days**", "**due TODAY**", "due tomorrow", "due Thu 12 Nov, 3 days"). Mark anything overdue or due within 2 days in bold. If the description has a checklist, show how many items are left ("2 of 4 steps left").
2. **🙋 Needs you:** from any project. Issues with the `needs-you` label, and colleague asks. A colleague ask is an `unstarted` issue that someone else created in the last 14 days. That is, `createdById` is set and is not `assigneeId`. A `backlog` issue is not a colleague ask, because the user has put it aside. Name the person who created it (`createdBy`). Show each one in full: what it asks, and the latest comment if it has one. Never shorten this section.
3. **🔴 Going stale:** state type `started`, and no change for more than 7 days (`updatedAt`). Give the days since the last change and the latest comment. Don't guess why it stopped. After the section, ask one question: "For each of these: paused on purpose, or stuck?" Don't wait for the answer. The user can answer in step 6. Don't change Linear because of the answer.
4. **🟢 Moving:** the other `started` issues, with the most recent change first. Use one line for each. Add "aging" if the last change was 3 to 7 days ago.
5. **📋 Ready:** `unstarted` issues with Urgent or High priority.
6. **Other Todo:** the other `unstarted` issues. Show only a count for each project. If the user says "show all", list them with numbers that continue the sequence.

In sections 3 to 5, and in Other Todo after "show all", add "(from <name>)" to an issue that someone else created. Sections 3 to 6 and Done recently show only the projects to show, and leave out the projects to skip. Leave out an empty section. Don't list `backlog` issues except in Due soon and Needs you.

Then add one line, **✅ Done recently**, that lists the IDs of the done issues. Don't number it.

**Show only top-level issues.** Hide an open issue only if its parent is also listed in this digest. Add "(N sub-issues)" to the parent's line, where N counts the hidden sub-issues. A parent that appears only in the Other Todo count is not listed. Show a sub-issue anyway if it's in Due soon, Needs you or Going stale. If the user asks to expand an issue, or asks to see sub-issues, list its open sub-issues under it.

**Layout.** Start with a count line right after the sync line, for example "1 due soon · 2 need you · 1 stale · 5 moving · 4 ready · 9 other todo · 6 done". Count only the items that you list. Number all the items in one sequence, from Due soon down, so the user can pick by number. For each item, show the ID, the title, the status if it isn't Todo, and the priority and due date when they're set.

Don't add the `needs-you` label or a comment to a colleague ask. This step only reads Linear.

## 3. Email

Search Gmail with the email query from the settings (pageSize 25, view `THREAD_VIEW_SUMMARY`). List the sender, subject and a few words on what it's about. Mark the ones that look like they need a reply or action. If there are more than about 15, show the most important and give a count of the rest.

## 4. Discord DMs (from email notifications)

Skip this step if the setting is "no". Bots can't see a person's Discord DMs, so use Discord's notification emails instead. Search Gmail with `from:discord.com newer_than:Nd`, where N is the number of days since the date in the state file (minimum 1, maximum 7, default 2). Keep only notifications about **DMs or mentions**: who messaged and any snippet. Skip marketing and security emails. If there are none, say so in one line.

## 5. Last line

If the settings give a last line for the digest, end the digest with it.

## 6. Ask what to focus on, then write the checklist

First recommend one or two items from step 2, with one sentence on why. Use this order of preference:

1. Items that are overdue or due within 2 days.
2. Needs you.
3. Going stale.
4. Urgent items in Ready.
5. The top item in Moving.

If all of these are empty, say that nothing is urgent. Then ask: **"Which do you want to focus on today?"** The user can reply with numbers from step 2 and/or new free-text items. Wait for the answer. If the user says that a Going stale item is stuck, offer to add it to the focus list. Don't change Linear because of a stale answer. If the user doesn't pick a Due soon item that is due within 2 days, name it and ask once if they want to add it.

Then add the chosen items to today's note (`<daily notes folder>/<today>.md`):

- If the note doesn't exist, create it containing only the section below.
- If it exists, **don't change anything already in it.** Add the section at the end, after a blank line.
- If a `## Focus` section is already there (for example, the digest already ran today), only add items that aren't listed yet.

Format, with **the Linear ID on every Linear item**, because step 1 relies on it tomorrow:

```markdown
## Focus
- [ ] Write the eval plan · [ENG-58](<workspace URL>/issue/ENG-58)
- [ ] Free-text item the user added · [ENG-60](<workspace URL>/issue/ENG-60)
```

**Every task becomes a Linear issue.** Don't ask first. For each free-text item, search with `list_issues` in the team, with `query` and no assignee filter. If an issue matches but isn't assigned to the user, say so and ask whether to assign it to them. If no issue matches, create one with `assignee: "me"` in the project that fits best. Follow any naming rules in `~/.agents/personal.md`. Say which project you chose. Put the new ID on the checklist line. This also applies to new tasks that the user mentions later in the session.

## 7. Finish

Write today's date to `~/.local/state/daily-digest/last-run` (create the folder if needed). End with one line confirming what was written to the note. If `~/.agents/personal.md` has a `## Standup settings` section, then ask: "Want me to draft your standup?" If the user says yes, use the `draft-standup` skill.

For the rest of the session, today's `## Focus` section is the to-do list. When the user finishes something, tick it there and mark its Linear issue Done. When they add something, create a Linear issue for it with `assignee: "me"`, and add a checkbox only if it's for today.
