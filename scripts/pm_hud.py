#!/usr/bin/env python3
"""An always-on-top HUD that renders the latest `pm-orient` read.

This is a dumb renderer on purpose. It does not talk to a tracker and needs no
API key: it displays a JSON file that the agent writes at the end of a check-in
(see the `pm-hud` skill for the schema). A saved tracker view can already show a
filtered list; what it cannot show is judgment — what needs you and why, what is
quietly going stale. That judgment is the whole reason this window exists.

Because the content is a snapshot, the age of the read is displayed as
prominently as the content itself, and goes amber then red as it ages. A stale
HUD should look stale.

    python3 pm_hud.py                    # render ~/.config/pm/hud.json
    python3 pm_hud.py --file other.json
    python3 pm_hud.py --scale 1.4        # start larger
    python3 pm_hud.py --once             # print to stdout and exit

Click a row to open it. Drag to move. A+ / A- (or ⌘+ / ⌘- / ⌘0) resize the
text; the window grows to fit and the choice persists. × / Esc / ⌘Q to quit.
"""
import argparse, json, pathlib, sys, webbrowser
from datetime import datetime, timezone

DEFAULT_FILE = pathlib.Path.home() / ".config" / "pm" / "hud.json"
STATE = pathlib.Path.home() / ".config" / "pm" / "hud_window.json"

BG, FG, DIM = "#15171c", "#e6e8ee", "#7d8496"
TONE = {"urgent": "#f2a25c", "active": "#5cc8f2", "warn": "#e0b34a",
        "done": "#6fbf73", "plain": "#c3c8d4"}
FRESH, AGING = 6 * 3600, 24 * 3600   # seconds before the timestamp goes amber, then red

FAMILY = "SF Pro Text"
# Point sizes at scale 1.0. Everything on screen derives from these.
FONTS = {"headline": (11, "bold"), "btn": (12, ""), "section": (8, "bold"),
         "item": (10, ""), "note": (9, ""), "footer": (9, "")}
SCALE_MIN, SCALE_MAX, SCALE_STEP = 0.8, 2.4, 0.15


def read_snapshot(path):
    """Return (data, error). Never raises — a broken file must still render."""
    try:
        return json.loads(path.read_text()), None
    except FileNotFoundError:
        return None, f"No read yet.\nRun pm-orient, or write\n{path}"
    except json.JSONDecodeError as e:
        return None, f"Malformed JSON in\n{path.name}\nline {e.lineno}: {e.msg}"
    except OSError as e:
        return None, f"Cannot read {path.name}:\n{e}"


def age_seconds(iso):
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).total_seconds()


def age_label(secs):
    if secs is None:
        return "age unknown", TONE["warn"]
    if secs < 90:
        return "just now", DIM
    if secs < 3600:
        return f"as of {int(secs // 60)}m ago", DIM
    if secs < FRESH:
        return f"as of {int(secs // 3600)}h ago", DIM
    if secs < AGING:
        return f"as of {int(secs // 3600)}h ago", TONE["warn"]
    return f"as of {int(secs // 86400)}d ago — re-run pm-orient", TONE["urgent"]


def render_text(data):
    lines = []
    if data.get("headline"):
        lines.append(data["headline"])
    for sec in data.get("sections", []):
        items = sec.get("items") or []
        if not items:
            continue
        lines.append(f"\n{sec.get('label', '').upper()}")
        for it in items:
            key = f"{it['key']}  " if it.get("key") else ""
            note = f"   ({it['note']})" if it.get("note") else ""
            lines.append(f"  {key}{it.get('text', '')}{note}")
    if data.get("next"):
        lines.append(f"\nNEXT: {data['next']}")
    lines.append(f"\n{age_label(age_seconds(data.get('generated_at')))[0]}")
    return "\n".join(lines)


class HUD:
    def __init__(self, args):
        import tkinter as tk

        self.tk, self.args, self.path = tk, args, args.file
        self.stamp, self.data = None, None
        saved = self._load_state()
        self.scale = args.scale if args.scale else saved.get("scale", 1.0)
        self.scale = min(SCALE_MAX, max(SCALE_MIN, self.scale))

        self.root = tk.Tk()
        self.root.title("pm")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-alpha", args.opacity)
        except tk.TclError:
            pass
        self.root.configure(bg=BG)
        self._place(saved)

        self.frame = tk.Frame(self.root, bg=BG, padx=11, pady=9)
        self.frame.pack(fill="both", expand=True)

        head = tk.Frame(self.frame, bg=BG)
        head.pack(fill="x")
        self.headline = tk.Label(head, text="", bg=BG, fg=FG, anchor="w", justify="left")
        self.headline.pack(side="left", fill="x", expand=True)
        # Packed right-to-left, so declare in reverse of the order you want to see.
        self.buttons = []
        for txt, cmd in (("×", self.quit), ("↻", self.reload),
                         ("A+", lambda: self.bump(+1)), ("A−", lambda: self.bump(-1))):
            btn = tk.Label(head, text=txt, bg=BG, fg=DIM, cursor="pointinghand")
            btn.pack(side="right", padx=(5, 0))
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            self.buttons.append(btn)

        self.body = tk.Frame(self.frame, bg=BG)
        self.body.pack(fill="both", expand=True, pady=(6, 0))
        self.footer = tk.Label(self.frame, text="", bg=BG, fg=DIM, anchor="w", justify="left")
        self.footer.pack(fill="x", pady=(7, 0))

        for w in (self.root, self.frame, self.headline, self.body, self.footer):
            w.bind("<ButtonPress-1>", self._drag_start)
            w.bind("<B1-Motion>", self._drag)
        self.root.bind("<Command-q>", lambda e: self.quit())
        self.root.bind("<Escape>", lambda e: self.quit())
        for seq in ("<Command-plus>", "<Command-equal>", "<Command-KP_Add>"):
            self.root.bind(seq, lambda e: self.bump(+1))
        for seq in ("<Command-minus>", "<Command-KP_Subtract>"):
            self.root.bind(seq, lambda e: self.bump(-1))
        self.root.bind("<Command-0>", lambda e: self.bump(0, reset=True))

        self._apply_fonts()
        self.reload()
        self._watch()
        self.root.mainloop()

    # ---- text size ------------------------------------------------------
    def font(self, role):
        size, weight = FONTS[role]
        scaled = max(7, round(size * self.scale))
        return (FAMILY, scaled, weight) if weight else (FAMILY, scaled)

    @property
    def width(self):
        """Grow the window with the text, or large type just wraps into a column."""
        want = round(self.args.width * self.scale)
        return min(want, self.root.winfo_screenwidth() - 40)

    def wrap(self, inset=0):
        return max(80, self.width - 26 - inset)

    def bump(self, direction, reset=False):
        new = 1.0 if reset else self.scale + direction * SCALE_STEP
        new = min(SCALE_MAX, max(SCALE_MIN, round(new, 3)))
        if new == self.scale:
            return
        self.scale = new
        self._apply_fonts()
        self.reload()          # rebuilds the body at the new size
        self._save_state()

    def _apply_fonts(self):
        self.headline.config(font=self.font("headline"), wraplength=self.wrap(46))
        self.footer.config(font=self.font("footer"), wraplength=self.wrap())
        for b in self.buttons:
            b.config(font=self.font("btn"))

    # ---- window position and size ---------------------------------------
    def _load_state(self):
        try:
            return json.loads(STATE.read_text())
        except Exception:
            return {}

    def _place(self, saved):
        w = round(self.args.width * self.scale)
        x = saved.get("x", self.root.winfo_screenwidth() - w - 24)
        y = saved.get("y", 48)
        self.root.geometry(f"{w}x300+{x}+{y}")

    def _fit(self):
        """Size the window to its content so a text bump can't clip the last row."""
        self.root.update_idletasks()
        h = min(self.frame.winfo_reqheight(), self.root.winfo_screenheight() - 120)
        self.root.geometry(f"{self.width}x{h}+{self.root.winfo_x()}+{self.root.winfo_y()}")

    def _save_state(self):
        try:
            STATE.parent.mkdir(parents=True, exist_ok=True)
            STATE.write_text(json.dumps({"x": self.root.winfo_x(), "y": self.root.winfo_y(),
                                         "scale": self.scale}))
        except OSError:
            pass

    def _drag_start(self, e):
        self._dx, self._dy = e.x_root - self.root.winfo_x(), e.y_root - self.root.winfo_y()

    def _drag(self, e):
        self.root.geometry(f"+{e.x_root - self._dx}+{e.y_root - self._dy}")

    def quit(self):
        self._save_state()
        self.root.destroy()

    # ---- refresh --------------------------------------------------------
    def _watch(self):
        """Reload when the file changes; otherwise just re-tick the age label."""
        try:
            stamp = self.path.stat().st_mtime
        except OSError:
            stamp = None
        if stamp != self.stamp:
            self.reload()
        else:
            self._render_footer(self.data or {})
        self.root.after(3000, self._watch)

    def reload(self):
        try:
            self.stamp = self.path.stat().st_mtime
        except OSError:
            self.stamp = None
        self.data, err = read_snapshot(self.path)
        for w in self.body.winfo_children():
            w.destroy()
        if err:
            self.headline.config(text="pm")
            self.tk.Label(self.body, text=err, bg=BG, fg=TONE["warn"], justify="left",
                          anchor="w", font=self.font("item"),
                          wraplength=self.wrap()).pack(fill="x")
            self.footer.config(text="")
        else:
            self._render(self.data)
        self._fit()

    def _render(self, data):
        self.headline.config(text=data.get("headline") or "pm")
        shown = 0
        for sec in data.get("sections", []):
            items = sec.get("items") or []
            if not items:
                continue
            colour = TONE.get(sec.get("tone", "plain"), TONE["plain"])
            self.tk.Label(self.body, text=sec.get("label", "").upper(), bg=BG, fg=DIM,
                          font=self.font("section"), anchor="w").pack(fill="x", pady=(6, 1))
            for it in items:
                if shown >= self.args.max_rows:
                    break
                shown += 1
                text = (f"{it['key']}  " if it.get("key") else "") + str(it.get("text", ""))
                lbl = self.tk.Label(self.body, text=text, bg=BG, fg=colour, anchor="w",
                                    font=self.font("item"), justify="left",
                                    wraplength=self.wrap(),
                                    cursor="pointinghand" if it.get("url") else "")
                lbl.pack(fill="x")
                if it.get("url"):
                    lbl.bind("<Button-1>", lambda e, u=it["url"]: webbrowser.open(u))
                if it.get("note"):
                    self.tk.Label(self.body, text=it["note"], bg=BG, fg=DIM, anchor="w",
                                  font=self.font("note"), justify="left",
                                  wraplength=self.wrap(10)).pack(fill="x", padx=(10, 0))
        if data.get("next"):
            self.tk.Label(self.body, text="NEXT", bg=BG, fg=DIM, font=self.font("section"),
                          anchor="w").pack(fill="x", pady=(8, 1))
            self.tk.Label(self.body, text=data["next"], bg=BG, fg=FG, anchor="w",
                          font=self.font("item"), justify="left",
                          wraplength=self.wrap()).pack(fill="x")
        self._render_footer(data)

    def _render_footer(self, data):
        label, colour = age_label(age_seconds(data.get("generated_at")))
        self.footer.config(text=label, fg=colour)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", type=pathlib.Path, default=DEFAULT_FILE)
    p.add_argument("--once", action="store_true", help="print to stdout and exit")
    p.add_argument("--scale", type=float, help=f"text size {SCALE_MIN}-{SCALE_MAX} (default: remembered)")
    p.add_argument("--max-rows", type=int, default=14)
    p.add_argument("--width", type=int, default=330, help="width at scale 1.0")
    p.add_argument("--opacity", type=float, default=0.95)
    args = p.parse_args()

    if args.once:
        data, err = read_snapshot(args.file)
        if err:
            sys.exit(err)
        print(render_text(data))
        return
    HUD(args)


if __name__ == "__main__":
    main()
