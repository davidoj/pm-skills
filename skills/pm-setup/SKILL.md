---
name: pm-setup
description: Install or repair the pm-skills system on a machine — make the skills visible from every directory, register and authenticate the MCP server for the active backend, and verify the adapter matches reality. Use on a new machine, after switching trackers, or when a session finds the pm-* skills or backend tools missing.
---

# pm-setup — make the system available and correct

**Serves:** Flow Continuity, Delegation Readiness (`PRINCIPLES.md`).

## Why this moment matters

Every other skill assumes two things are true: that it can be found from
whatever directory the user happens to be in, and that the tools its adapter
names actually exist in the session. When either is false the failure is
silent and expensive — the agent doesn't announce "I can't see pm-orient", it
just works without it, and the user gets an ordinary unstructured session and
wonders why the system isn't helping.

This skill is the one place that checks.

## The result you're producing

At the end, all four of these are verified true — not assumed:

1. Every skill in `skills/` resolves from an arbitrary directory.
2. The backend named in `backends/ACTIVE.md` has working, authenticated tools
   in this session.
3. The adapter's workspace specifics (teams, labels, states, user) match what
   the backend actually returns.
4. The user knows which of the above you had to change.

If you cannot verify one, say which and why. A setup that reports success
without a live read is exactly the dashboard-that-lies failure the desiderata
warn about.

## 1 — Skills visible everywhere

Claude Code discovers user-level skills in `~/.claude/skills/`. Symlink rather
than copy, so editing the repo edits the live skill:

```bash
mkdir -p ~/.claude/skills
for s in ~/Dev/pm-skills/skills/*; do
  ln -sfn "$s" ~/.claude/skills/$(basename "$s")
done
ls -l ~/.claude/skills | grep pm-
```

Verify each link resolves (`ls -L`), and that every skill directory in the repo
got one — a skill added to the repo but never linked is the common failure.
Note that new skills are picked up at session start, so a freshly linked skill
may need a restart before it can be invoked.

## 2 — Backend tools present and authenticated

Read `backends/ACTIVE.md` first; it names the live backend and carries the
registration commands. Then check the session actually has the tools.

**Linear** (current backend):

```bash
claude mcp list | grep -i linear
# if absent:
claude mcp add --transport http --scope user linear-server https://mcp.linear.app/mcp
```

`--scope user` matters: project scope only surfaces the tools inside that one
repo, which is precisely the "works at my desk" failure this skill exists to
prevent. After adding, the user runs `/mcp` once to complete OAuth, and
restarts the session.

Sessions started *before* registration will not have the tools no matter what
you do — say so rather than retrying. The fallback for those is
`scripts/linear_apply_plan.py` (GraphQL, needs `LINEAR_API_KEY`).

**Verify with a live read**, not by the presence of the tool: list teams and
projects and confirm you get real data back.

## 3 — Adapter matches reality

`backends/ACTIVE.md` records workspace specifics — team keys, label names,
workflow states, the user identity. These drift. Check them against a live
read and reconcile:

- Do the team keys still exist and mean what the doc says?
- Do the labels the skills rely on exist? (`needs-you` is load-bearing for
  `pm-orient` and `pm-hud`; `blocked` may still be uncreated.)
- Are the workflow state names unchanged? Prefer filtering on state *type*
  over state *name* wherever the adapter can.

Where practice has genuinely moved on, this is `pm-tune`'s job, not yours —
hand it over rather than rewriting the spec here.

## 4 — Offer the pinned window

On a primary workstation (skip it on a server), offer it in a line:

> If you want a curated to-do list on screen, run
> `python3 ~/Dev/pm-skills/scripts/pm_hud.py`

It renders `~/.config/pm/hud.json`, so run `pm-orient` first if that file
doesn't exist yet. Controls: drag to move, `A+`/`A−` for text size, click a row
to open it, `Esc` to quit.

It's a small tkinter window and machines differ — if it doesn't appear or looks
wrong, debug it with them there and then. The LaunchAgent in `pm-hud` is for
surviving a reboot; mention it only if they ask.

## Report back

Say plainly what you changed, what was already correct, and what you could not
verify from this session. Then name the next step — usually `pm-orient`, since
a freshly wired-up system's first job is to tell the user where things stand.
