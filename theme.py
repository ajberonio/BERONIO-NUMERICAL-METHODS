# ─────────────────────────────────────────────
#  theme.py  —  shared colors, fonts, widgets
#  Import this in any GUI file that needs styling
# ─────────────────────────────────────────────
import tkinter as tk

# ── Colors ────────────────────────────────────
BG        = "#f0f6ff"
PANEL     = "#dbeafe"
BORDER    = "#93c5fd"
ACCENT    = "#2563eb"
ACCENT2   = "#0ea5e9"
TEXT      = "#1e3a5f"
TEXT_DIM  = "#64748b"
SUCCESS   = "#15803d"
ERROR_CLR = "#dc2626"
ENTRY_BG  = "#ffffff"
BTN_HOVER = "#1d4ed8"
GRAPH_BG  = "#f8fbff"

# ── Fonts ─────────────────────────────────────
FONT_TITLE = ("Courier New", 14, "bold")
FONT_LABEL = ("Courier New", 9,  "bold")
FONT_MONO  = ("Courier New", 10)
FONT_SMALL = ("Courier New", 8)


# ── Reusable styled button ────────────────────
class StyledButton(tk.Button):
    def __init__(self, parent, text, command, color=ACCENT, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            bg=color, fg="#ffffff",
            activebackground=BTN_HOVER, activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            font=FONT_LABEL, padx=10, pady=6, **kwargs,
        )
        self._color = color
        self.bind("<Enter>", lambda _: self.config(bg=self._darken(color)))
        self.bind("<Leave>", lambda _: self.config(bg=color))

    @staticmethod
    def _darken(hex_color: str) -> str:
        r, g, b = (int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        return "#{:02x}{:02x}{:02x}".format(
            max(0, r - 30), max(0, g - 30), max(0, b - 30))


# ── Reusable error popup ──────────────────────
def show_error_popup(win, msg: str):
    popup = tk.Toplevel(win)
    popup.title("Input Error")
    popup.configure(bg=BG)
    popup.resizable(False, False)
    popup.grab_set()

    tk.Frame(popup, bg=ERROR_CLR, height=4).pack(fill="x")
    tk.Label(popup, text="⚠  Invalid Input", font=FONT_LABEL,
             bg=BG, fg=ERROR_CLR).pack(anchor="w", padx=20, pady=(14, 4))
    tk.Label(popup, text=msg, font=FONT_MONO, bg=BG, fg=TEXT,
             justify="left", wraplength=340).pack(anchor="w", padx=20, pady=(0, 14))
    StyledButton(popup, "OK", popup.destroy, color=ACCENT).pack(pady=(0, 14))

    popup.update_idletasks()
    x = win.winfo_x() + (win.winfo_width()  - popup.winfo_width())  // 2
    y = win.winfo_y() + (win.winfo_height() - popup.winfo_height()) // 2
    popup.geometry(f"+{x}+{y}")