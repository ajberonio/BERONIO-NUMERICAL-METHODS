# ─────────────────────────────────────────────
#  root_gui.py  —  Refined Root Finding Tab
# ─────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from methods.incremental import incremental
from methods.bisection import bisection
from methods.false_position import false_position
from methods.newton_raphson import newton_raphson
from methods.secant import secant

# Theme token configurations imported safely from theme module
from theme import (BG, PANEL, BORDER, ACCENT, TEXT, TEXT_DIM,
                   ERROR_CLR, ENTRY_BG, GRAPH_BG,
                   FONT_TITLE, FONT_LABEL, FONT_MONO, FONT_SMALL,
                   StyledButton, show_error_popup)

# Custom small font variant without the unrecognized Tkinter "medium" string
FONT_SMALL_FIXED = (FONT_SMALL[0], FONT_SMALL[1], "normal")

METHOD_COLUMNS = {
    "Incremental":    (("Iteration","xl","Δx","xu","f(xl)","f(xu)","f(xl)·f(xu)","Remark"), 75),
    "Bisection":      (("Iteration","xl","xr","xu","f(xl)","f(xr)","|Ea|,%","f(xl)·f(xr)","Remark"), 68),
    "False Position": (("Iteration","XL","XU","XR","Ea","f(XL)","f(XU)","f(XR)","f(XL)*f(XR)"), 68),
    "Newton-Raphson": (("No. of Iteration","Xi","|Ea|,%","f(Xi)","f'(Xi)"), 95),
    "Secant":         (("Iteration Number","Xi-1","Xi","Xi+1","|Ea|,%","f(Xi-1)","f(Xi)","f(Xi+1)"), 80),
}

ENTRY_HINTS = {
    "Equation":  "e.g.  e^(-x) - x",
    "Xl":        "e.g.  0",
    "Xu":        "e.g.  1",
    "Tolerance": "e.g.  0.001",
}

def _make_entry(parent, label, row):
    """Produces clean form components using cohesive border colors instead of pure black lines."""
    lbl = tk.Label(parent, text=label, font=FONT_LABEL, bg=PANEL, fg=TEXT, anchor="w")
    lbl.grid(row=row, column=0, sticky="w", padx=(14, 6), pady=(4, 4))

    entry = tk.Entry(parent, font=FONT_MONO, bg=ENTRY_BG, fg=TEXT_DIM,
                     insertbackground=ACCENT, relief="solid", bd=1,
                     highlightthickness=1, highlightcolor=ACCENT,
                     highlightbackground=BORDER)
    entry.grid(row=row, column=1, sticky="ew", padx=(0, 14), pady=(4, 4))

    hint = ENTRY_HINTS.get(label, "")
    entry.insert(0, hint)
    entry._has_hint = True

    def on_focus_in(e):
        if entry._has_hint:
            entry.delete(0, tk.END)
            entry.config(fg=TEXT)
            entry._has_hint = False

    def on_focus_out(e):
        if not entry.get().strip():
            entry.insert(0, hint)
            entry.config(fg=TEXT_DIM)
            entry._has_hint = True

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

def build(parent, win):
    parent.columnconfigure(1, weight=1)
    parent.rowconfigure(0, weight=1)

    # ── LEFT STRUCTURAL PARAMETER SIDEBAR ────────────────────────────────
    sidebar = tk.Frame(parent, bg=PANEL, width=320, highlightthickness=1, highlightbackground=BORDER)
    sidebar.grid(row=0, column=0, sticky="ns", padx=(10, 10), pady=10)
    sidebar.grid_propagate(False)
    sidebar.columnconfigure(1, weight=1)

    hdr = tk.Frame(sidebar, bg=BORDER, pady=8)
    hdr.grid(row=0, column=0, columnspan=2, sticky="ew")
    tk.Label(hdr, text="PROPERTIES & CONSTANTS", font=FONT_LABEL, bg=BORDER, fg=TEXT_DIM).pack(side="left", padx=12)

    # Core Form Generation Matrix
    eq_entry = _make_entry(sidebar, "Equation",  1)

    # Cleaned, unified Equation Helper Shortcuts panel
    ex_frame = tk.Frame(sidebar, bg=BG, highlightthickness=1, highlightbackground=BORDER)
    ex_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(2, 6))
    tk.Label(ex_frame, text="Preset Mathematical Profiles:", font=FONT_SMALL_FIXED, bg=BG, fg=ACCENT, anchor="w").pack(fill="x", padx=6, pady=(4, 2))

    EXAMPLES = [
        ("e^(-x) - x",         "Incremental / Bisection"),
        ("x^3 - x - 2",        "Bisection"),
        ("3*x + sin(x) - e^x", "False Position / NR"),
    ]

    for eq_text, hint_text in EXAMPLES:
        row_f = tk.Frame(ex_frame, bg=BG, cursor="hand2")
        row_f.pack(fill="x", padx=4, pady=1)
        tk.Label(row_f, text=eq_text, font=FONT_MONO, bg=BG, fg=TEXT, anchor="w").pack(side="left", padx=(2,0))
        tk.Label(row_f, text=f" ({hint_text})", font=FONT_SMALL_FIXED, bg=BG, fg=TEXT_DIM, anchor="w").pack(side="left")

        def _click(e, eq=eq_text):
            eq_entry.config(fg=TEXT)
            eq_entry._has_hint = False
            eq_entry.delete(0, tk.END)
            eq_entry.insert(0, eq)
        row_f.bind("<Button-1>", _click)
        for child in row_f.winfo_children(): child.bind("<Button-1>", _click)

    # Method Selector Form Blocks
    tk.Label(sidebar, text="Method", font=FONT_LABEL, bg=PANEL, fg=TEXT, anchor="w").grid(row=3, column=0, sticky="w", padx=(14, 6), pady=(6, 4))
    method_var = tk.StringVar(value="Incremental")
    method_combo = ttk.Combobox(sidebar, textvariable=method_var, values=list(METHOD_COLUMNS.keys()), state="readonly", font=FONT_MONO)
    method_combo.grid(row=3, column=1, sticky="ew", padx=(0, 14), pady=(6, 4))

    xu_hint = tk.Label(sidebar, text="", font=FONT_SMALL_FIXED, bg=PANEL, fg=ERROR_CLR, anchor="w", wraplength=180)
    xu_hint.grid(row=4, column=0, columnspan=2, sticky="w", padx=14, pady=(0, 2))

    xl_entry = _make_entry(sidebar, "Xl", 5)
    xu_entry = _make_entry(sidebar, "Xu", 6)

    tk.Frame(sidebar, bg=BORDER, height=1).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 4))
    tk.Label(sidebar, text="Stopping Criteria", font=FONT_LABEL, bg=PANEL, fg=TEXT, anchor="w").grid(row=8, column=0, columnspan=2, sticky="w", padx=14, pady=(2, 2))

    tol_entry = _make_entry(sidebar, "Tolerance", 9)

    # Step Delta Layout Modules
    dx_label = tk.Label(sidebar, text="Dx =", font=FONT_LABEL, bg=PANEL, fg=TEXT, anchor="w")
    dx_label.grid(row=10, column=0, sticky="w", padx=(14, 4), pady=(4, 4))
    dx_entry = tk.Entry(sidebar, font=FONT_MONO, bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT, relief="solid", bd=1, width=8, highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)
    dx_entry.grid(row=10, column=1, sticky="w", padx=(0, 14), pady=(4, 4))
    dx_entry.insert(0, "0.5")

    def on_method_change(event=None):
        method = method_var.get()
        if method in ("Newton-Raphson", "Incremental"):
            xu_entry.config(state="disabled", bg="#e2e8f0", fg=TEXT_DIM)
            xu_hint.config(text=f"※ Range bounded dynamically via step profile." if method=="Incremental" else "※ Derivative evaluation avoids bound dependency.")
        else:
            xu_entry.config(state="normal", bg=ENTRY_BG, fg=TEXT)
            xu_hint.config(text="")
            
        if method == "Incremental":
            dx_label.grid(); dx_entry.grid()
        else:
            dx_label.grid_remove(); dx_entry.grid_remove()

    method_combo.bind("<<ComboboxSelected>>", on_method_change)
    on_method_change()

    # Footer Operations Row
    tk.Frame(sidebar, bg=BORDER, height=1).grid(row=13, column=0, columnspan=2, sticky="ew", pady=(8, 4))
    status_var = tk.StringVar(value="● SYSTEM READY")
    tk.Label(sidebar, textvariable=status_var, font=FONT_SMALL_FIXED, bg=PANEL, fg=TEXT_DIM, justify="left").grid(row=14, column=0, columnspan=2, sticky="w", padx=14, pady=(2, 6))

    # Styled Buttons integrated smoothly side by side
    StyledButton(sidebar, "COMPUTE SYSTEM", lambda: solve(), color=ACCENT).grid(row=16, column=0, columnspan=2, sticky="ew", padx=14, pady=3)
    StyledButton(sidebar, "RESET FLUSH", lambda: clear_all(), color="#94a3b8").grid(row=17, column=0, columnspan=2, sticky="ew", padx=14, pady=(3, 12))

    # ── RIGHT RESULTS DISPLAY COMPONENT MATRIX ───────────────────────────
    right = tk.Frame(parent, bg=BG)
    right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
    right.columnconfigure(0, weight=1)
    right.rowconfigure(2, weight=1)

    result_frame = tk.Frame(right, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    result_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    result_var = tk.StringVar(value="Identified Critical Root Coordinate:  —")
    tk.Label(result_frame, textvariable=result_var, font=FONT_TITLE, bg=PANEL, fg=ACCENT).pack(side="left", padx=14, pady=8)
    ea_var = tk.StringVar(value="")
    tk.Label(result_frame, textvariable=ea_var, font=FONT_SMALL_FIXED, bg=PANEL, fg=TEXT_DIM).pack(side="right", padx=14, pady=8)

    graph_frame = tk.Frame(right, bg=PANEL, height=280, highlightthickness=1, highlightbackground=BORDER)
    graph_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    graph_frame.grid_propagate(False)

    fig = Figure(figsize=(6, 3.0), dpi=96, facecolor=GRAPH_BG)
    ax  = fig.add_subplot(111)
    ax.set_facecolor(GRAPH_BG)
    fig.tight_layout(pad=2.0)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    table_frame = tk.Frame(right, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    table_frame.grid(row=2, column=0, sticky="nsew")
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Root.Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL, font=("Consolas", 9), rowheight=24)
    style.configure("Root.Treeview.Heading", background=BORDER, foreground=TEXT, font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Root.Treeview", background=[("selected", ACCENT)], foreground=[("selected", "#ffffff")])

    init_cols = METHOD_COLUMNS["Bisection"][0]
    tree = ttk.Treeview(table_frame, columns=init_cols, show="headings", style="Root.Treeview")
    for col in init_cols:
        tree.heading(col, text=col)
        tree.column(col, width=75, anchor="center")
    
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    def _get_float(entry, name):
        val = entry.get().strip()
        if not val or getattr(entry, "_has_hint", False):
            raise ValueError(f"Operational missing field target: {name}")
        try: return float(val)
        except ValueError: raise ValueError(f"Target variable '{val}' is non-numeric format.")

    def _parse_equation(raw: str) -> str:
        import re
        # 1. Strip all blank spaces so 'sin (x)' becomes 'sin(x)' immediately
        eq = raw.replace(" ", "").strip()

        # 2. Add explicit multiplication signs where implicit multiplication is used
        eq = re.sub(r'(\d)(x)', r'\1*\2', eq)
        eq = re.sub(r'(\d)(\()', r'\1*\2', eq)
        eq = re.sub(r'(x)(\()', r'\1*\2', eq)
        eq = re.sub(r'(\))(x)', r'\1*\2', eq)
        eq = re.sub(r'(\))(\d)', r'\1*\2', eq)
        eq = eq.replace("^", "**")

        # 3. Handle specific Euler constants and Pi symbols
        eq = re.sub(r'(?<![a-zA-Z])e(?![a-zA-Z\d_])', 'math.e', eq)
        eq = eq.replace("pi", "math.pi")

        # 4. Safely map human math names to Python's math library syntax
        replacements = [
            ("ln(",    "math.log("),
            ("log10(", "math.log10("),
            ("log2(",  "math.log2("),
            ("log(",   "math.log10("),
            ("exp(",   "math.exp("),
            ("sqrt(",  "math.sqrt("),
            ("cbrt(",  "math.pow("),
            ("sind(",  "math.sin(math.radians("),
            ("cosd(",  "math.cos(math.radians("),
            ("tand(",  "math.tan(math.radians("),
            ("sin(",   "math.sin("),
            ("cos(",   "math.cos("),
            ("tan(",   "math.tan("),
            ("asin(",  "math.asin("),
            ("acos(",  "math.acos("),
            ("atan(",  "math.atan("),
            ("sinh(",  "math.sinh("),
            ("cosh(",  "math.cosh("),
            ("tanh(",  "math.tanh("),
            ("abs(",   "abs("),
        ]
        for human, python in replacements:
            eq = eq.replace(human, python)

        return eq

    def _get_equation(entry):
        import math
        raw = entry.get().strip()
        if not raw or getattr(entry, "_has_hint", False): raise ValueError("Equation formula parameter unassigned.")
        eq = _parse_equation(raw)
        return lambda x: eval(eq, {"math": math, "x": x})

    def solve():
        status_var.set("⏳ PROCESSING STACK...")
        parent.update_idletasks()
        try:
            f = _get_equation(eq_entry)
            xl = _get_float(xl_entry, "Xl")
            method = method_var.get()
            
            xu = _get_float(xu_entry, "Xu") if method not in ("Newton-Raphson", "Incremental") else None
            tol = _get_float(tol_entry, "Tolerance") if method != "Incremental" else 0.001

            if method == "Incremental":
                dx = float(dx_entry.get().strip())
                root_val, iters = incremental(f, xl, xu, step=dx)
            else:
                if method == "Bisection": root_val, iters = bisection(f, xl, xu, tol)
                elif method == "False Position": root_val, iters = false_position(f, xl, xu, tol)
                elif method == "Newton-Raphson": root_val, iters = newton_raphson(f, xl, tol)
                elif method == "Secant": root_val, iters = secant(f, xl, xu, tol)

            for row in tree.get_children(): tree.delete(row)
            cols, col_w = METHOD_COLUMNS[method]
            tree["columns"] = cols
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=col_w, anchor="center")

            for row in iters: tree.insert("", tk.END, values=row)

            if root_val is not None:
                result_var.set(f"Identified Critical Root Coordinate:  {root_val:.6f}")
                ea_var.set(f"{len(iters)} Evaluation Passes | {method}")
                status_var.set("● EXECUTION SUCCESSFUL")
            else:
                result_var.set("Identified Critical Root Coordinate:  Not Located")
                status_var.set("⚠ ZERO INTERSECT NOT FOUND")

            ax.clear()
            ax.set_facecolor(GRAPH_BG)
            
            # Smart dynamic limit boundaries to prevent data boundary clipping
            if root_val is not None:
                x_start = min(xl, root_val) - 1.5
                x_end = max(xl + 3, root_val) + 1.5
            else:
                x_end = (xl + 5) if xu is None else xu
                x_start = xl - 1

            x_vals = np.linspace(x_start, x_end, 500)
            y_vals = [f(v) for v in x_vals]
            
            ax.plot(x_vals, y_vals, color=ACCENT, linewidth=2, label="f(x)")
            ax.axhline(0, color=BORDER, linewidth=1, linestyle="--")
            ax.axvline(0, color=BORDER, linewidth=1, linestyle="--")
            
            if root_val is not None:
                ax.plot(root_val, f(root_val), "o", color=ERROR_CLR, markersize=8, label=f"Root Int. ≈ {root_val:.4f}", zorder=5)
            
            ax.set_title(f"Mathematical Trace  —  System Convergence Model via {method}", fontsize=9, color=TEXT, loc="left")
            ax.tick_params(labelsize=7, colors=TEXT_DIM)
            ax.grid(True, color=ENTRY_BG, linewidth=1)
            ax.legend(fontsize=8, facecolor=GRAPH_BG, edgecolor="none")
            
            # Clean up the bounding graph borders
            for spine in ax.spines.values(): spine.set_edgecolor(BORDER)
            fig.tight_layout(pad=1.5)
            canvas.draw()

        except Exception as exc:
            status_var.set("● INTERRUPT ERROR")
            result_var.set("Identified Critical Root Coordinate:  —")
            show_error_popup(win, str(exc))

    def clear_all():
        for w in (eq_entry, xl_entry, xu_entry, tol_entry):
            w.delete(0, tk.END)
            w.event_generate("<FocusOut>")
        dx_entry.delete(0, tk.END); dx_entry.insert(0, "0.5")
        for row in tree.get_children(): tree.delete(row)
        ax.clear(); ax.set_facecolor(GRAPH_BG); canvas.draw()
        result_var.set("Identified Critical Root Coordinate:  —"); ea_var.set("")
        status_var.set("● REINITIALIZED SYSTEM")


if __name__ == "__main__":
    win = tk.Tk()
    win.title("Root Finding Methods")
    win.geometry("1100x660")
    win.minsize(900, 580)
    win.configure(bg=BG)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)

    header = tk.Frame(win, bg=PANEL, pady=10,
                      highlightthickness=1, highlightbackground=BORDER)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(1, weight=1)
    tk.Label(header, text="√", font=("Courier New", 20, "bold"),
             bg=PANEL, fg=ACCENT).grid(row=0, column=0, padx=(18, 8))
    tk.Label(header, text="ROOT FINDING METHODS", font=FONT_TITLE,
             bg=PANEL, fg=TEXT).grid(row=0, column=1, sticky="w")

    frame = tk.Frame(win, bg=BG)
    frame.grid(row=1, column=0, sticky="nsew")
    build(frame, win)
    win.mainloop()