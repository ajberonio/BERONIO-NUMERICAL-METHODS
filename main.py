# ─────────────────────────────────────────────
#  main.py  —  App entry point
#  Builds the nav bar and swaps tabs.
#  Each module lives in its own file.
# ─────────────────────────────────────────────
import tkinter as tk
import root_gui
import matrix_gui
from theme import (BG, PANEL, BORDER, ACCENT, TEXT, TEXT_DIM,
                   FONT_TITLE, FONT_LABEL, FONT_SMALL)

if __name__ == "__main__":
    win = tk.Tk()
    win.title("Numerical Methods System")
    win.geometry("1200x740")
    win.minsize(1000, 660)
    win.configure(bg=BG)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)

    # ── HEADER ────────────────────────────────────────────────────────────
    header = tk.Frame(win, bg=PANEL,
                      highlightthickness=1, highlightbackground=BORDER)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(2, weight=1)

    tk.Label(header, text="∑", font=("Courier New", 22, "bold"),
             bg=PANEL, fg=ACCENT).grid(row=0, column=0, padx=(18, 8), pady=10)
    tk.Label(header, text="NUMERICAL METHODS", font=FONT_TITLE,
             bg=PANEL, fg=TEXT).grid(row=0, column=1, sticky="w")

    # ── NAV BUTTONS ───────────────────────────────────────────────────────
    nav = tk.Frame(header, bg=PANEL)
    nav.grid(row=0, column=2, sticky="e", padx=18)

    # ── CONTENT AREA ──────────────────────────────────────────────────────
    content = tk.Frame(win, bg=BG)
    content.grid(row=1, column=0, sticky="nsew")
    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)

    root_frame   = tk.Frame(content, bg=BG)
    matrix_frame = tk.Frame(content, bg=BG)
    for f in (root_frame, matrix_frame):
        f.grid(row=0, column=0, sticky="nsew")

    # Build each module into its own frame — all logic stays in its own file
    root_gui.build(root_frame,   win)
    matrix_gui.build(matrix_frame, win)

    matrix_frame.grid_remove()   # hide matrix tab on startup

    # ── TAB SWITCHING ─────────────────────────────────────────────────────
    active_tab = tk.StringVar(value="root")

    TABS = [
        ("root",   "√  Root Finding", root_frame),
        ("matrix", "▦  Matrix Ops",   matrix_frame),
    ]

    nav_buttons = {}

    def switch_tab(key):
        active_tab.set(key)
        for k, _, frame in TABS:
            if k == key: frame.grid()
            else:        frame.grid_remove()
        _refresh_nav()

    def _refresh_nav():
        active = active_tab.get()
        for key, btn in nav_buttons.items():
            if key == active:
                btn.config(bg=ACCENT, fg="#ffffff")
            else:
                btn.config(bg=PANEL, fg=TEXT_DIM)

    for i, (key, label, _) in enumerate(TABS):
        btn = tk.Button(
            nav, text=label, font=FONT_LABEL,
            relief="flat", bd=0, cursor="hand2",
            padx=18, pady=10,
            command=lambda k=key: switch_tab(k),
        )
        btn.grid(row=0, column=i, sticky="ns")
        nav_buttons[key] = btn

    _refresh_nav()   # highlight first tab

    win.mainloop()