---
name: pm-hud
description: Write or troubleshoot the pinned always-on-top HUD that displays the latest pm-orient read. Use when the user asks for a pinned/floating status window, asks to refresh what the HUD is showing, or when the HUD shows an error or looks stale.
---

# pm-hud — the orient read, left on screen

**Serves:** Attention Routing, Truthful State (`PRINCIPLES.md`).

## Why this moment matters

Attention Routing normally happens because someone asked: the user opens a
session, `pm-orient` answers. The routing that matters most is the routing
nobody asked for — the glance between tasks that surfaces the ask which has
been waiting three days.

A saved tracker view shows which issues match a filter. It can't say *this needs
you because a reply hasn't come*, or *this has gone quiet — was that
deliberate?* That judgment is what `pm-orient` produces, and carrying it is the
only thing that justifies this window.

## The result you're producing

`~/.config/pm/hud.json` contains the current check-in, honestly timestamped, in
the schema below — and the user can see it without asking anyone anything.

## When to write it

At the end of any `pm-orient` run, and after any exchange that materially
changes what needs the user's attention — an ask answered, a blocker cleared, a
deadline discovered. Do not rewrite it on every message; a HUD that flickers is
a HUD that gets closed.

**Never write a timestamp you did not just earn.** `generated_at` means "this
is when I actually read the tracker". Refreshing the stamp without re-reading
is precisely the dashboard-that-lies failure — the display goes green while the
content rots, which is worse than showing an honest three-day-old read.

## Schema

```json
{
  "generated_at": "2026-09-07T10:20:00+10:00",
  "headline": "3 need you · 2 moving · 2 stale",
  "next": "Mentor form — 9 days out, ~2 min, no dependencies",
  "sections": [
    {
      "label": "needs you",
      "tone": "urgent",
      "items": [
        {"key": "ABC-11",
         "text": "Grant application: tax ID + admin contact",
         "note": "blocked on finance — ask early, due 25 Sep",
         "url": "https://linear.app/…/issue/ABC-11"}
      ]
    }
  ]
}
```

- `headline` — the same one-line summary `pm-orient` opens with.
- `next` — the recommendation `pm-orient` closes with. One action, not three.
- `tone` — `urgent` · `warn` · `active` · `done` · `plain`. Colour only.
- `key`, `note`, `url` are all optional; `text` is not.

Mirror `pm-orient`'s sections: **needs you** (`urgent`), **moving** (`active`),
**going stale** (`warn`). Keep the whole file under ~12 items. The fifty-item
wall routes no attention, and on a 330px window it routes even less.

## The renderer

`~/Dev/pm-skills/scripts/pm_hud.py` — stdlib only (tkinter), no network, no API
key. It renders the file, reloads within ~3s of any change, and ages the
timestamp from grey to amber (6h) to red (24h, "re-run pm-orient").

```bash
python3 ~/Dev/pm-skills/scripts/pm_hud.py           # the window
python3 ~/Dev/pm-skills/scripts/pm_hud.py --once    # same content as text
```

Drag to move. `A+` / `A−` (or `⌘+` / `⌘−`, `⌘0` to reset) change text size —
the window widens and grows to fit, so large type doesn't wrap into a column.
Position and text size persist in `~/.config/pm/hud_window.json`. Click a row
with a `url` to open it. `×`, `Esc` or `⌘Q` quits. Flags: `--file`, `--scale`,
`--width` (the width at scale 1.0), `--max-rows`, `--opacity`.

To survive a reboot, offer a LaunchAgent at
`~/Library/LaunchAgents/ai.pm-skills.hud.plist` running `pm_hud.py` with
`RunAtLoad`. Offer it; don't install it unasked.

## If they only want a list

A saved view in the tracker is better than this — point them at it.

## Troubleshooting

| Symptom | Cause |
|---|---|
| "No read yet" | `~/.config/pm/hud.json` absent. Run `pm-orient`. |
| "Malformed JSON" | The file was written mid-edit or by hand. The renderer names the line. |
| Timestamp red | The read is over a day old. That is the feature working. |
| Content never changes | Nothing has run `pm-orient` since. The renderer has no tracker access by design. |
| Window off-screen after a display change | `rm ~/.config/pm/hud_window.json`, relaunch. |

## Notes

- Backend-agnostic: the file is plain JSON, so swapping trackers per
  `backends/ACTIVE.md` changes who writes it, not the window.
- Read-only on purpose. If the user starts wanting to act from the HUD, that is
  `pm-pickup` asking to be used.
