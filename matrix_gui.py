# ─────────────────────────────────────────────
#  matrix_gui.py  —  Integrated Matrix GUI Module
# ─────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk
import numpy as np

# Importing your specific matrix script modules from the matrix_methods folder
from matrix_methods import addition
from matrix_methods import multiplication
from matrix_methods import determinant
from matrix_methods import inverse
from matrix_methods import transpose
from matrix_methods import power
from matrix_methods import equations
from matrix_methods import adjoint

# Linking core styling tokens and popups from your app configuration
from theme import (BG, PANEL, BORDER, ACCENT, TEXT, TEXT_DIM,
                   ERROR_CLR, ENTRY_BG, FONT_TITLE, FONT_LABEL, 
                   FONT_MONO, FONT_SMALL, StyledButton, show_error_popup)

FONT_SMALL_FIXED = (FONT_SMALL[0], FONT_SMALL[1], "normal")

def build(parent, win):
    parent.columnconfigure(0, weight=1)
    parent.rowconfigure(1, weight=1)

    # UI component trackers
    matrix_a_cells = []
    matrix_b_cells = []

    # ── TOP PARAMETER CONTROL BAR ──────────────────────────────────────
    control_bar = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    control_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
    
    # Dimension Selectors - Matrix A
    tk.Label(control_bar, text="Matrix A Size:", font=FONT_LABEL, bg=PANEL, fg=TEXT).pack(side="left", padx=(14, 4), pady=10)
    r_a_var = tk.StringVar(value="3"); c_a_var = tk.StringVar(value="3")
    combo_ra = ttk.Combobox(control_bar, textvariable=r_a_var, values=["1","2","3","4","5"], state="readonly", font=FONT_MONO, width=3)
    combo_ra.pack(side="left", padx=2)
    tk.Label(control_bar, text="x", font=FONT_LABEL, bg=PANEL, fg=TEXT_DIM).pack(side="left", padx=2)
    combo_ca = ttk.Combobox(control_bar, textvariable=c_a_var, values=["1","2","3","4","5"], state="readonly", font=FONT_MONO, width=3)
    combo_ca.pack(side="left", padx=2)

    # Dimension Selectors - Matrix B
    tk.Label(control_bar, text=" |  Matrix B Size:", font=FONT_LABEL, bg=PANEL, fg=TEXT_DIM).pack(side="left", padx=(10, 4))
    r_b_var = tk.StringVar(value="3"); c_b_var = tk.StringVar(value="3")
    combo_rb = ttk.Combobox(control_bar, textvariable=r_b_var, values=["1","2","3","4","5"], state="readonly", font=FONT_MONO, width=3)
    combo_rb.pack(side="left", padx=2)
    tk.Label(control_bar, text="x", font=FONT_LABEL, bg=PANEL, fg=TEXT_DIM).pack(side="left", padx=2)
    combo_cb = ttk.Combobox(control_bar, textvariable=c_b_var, values=["1","2","3","4","5"], state="readonly", font=FONT_MONO, width=3)
    combo_cb.pack(side="left", padx=2)

    # Power Input Exponent (k Factor)
    tk.Label(control_bar, text=" |  Exponent (k):", font=FONT_LABEL, bg=PANEL, fg=TEXT).pack(side="left", padx=(14, 4))
    power_var = tk.StringVar(value="2")
    power_combo = ttk.Combobox(control_bar, textvariable=power_var, values=["2","3","4","5"], state="readonly", font=FONT_MONO, width=3)
    power_combo.pack(side="left", padx=2)

    # ── MAIN WORKSPACE CONTAINER ─────────────────────────────────────────
    workspace = tk.Frame(parent, bg=BG)
    workspace.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    workspace.columnconfigure(0, weight=1) 
    workspace.columnconfigure(1, weight=1) 
    workspace.rowconfigure(0, weight=1)

    # Left Container Card: Layout inputs
    left_card = tk.Frame(workspace, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    left_card.rowconfigure(1, weight=1)
    left_card.columnconfigure(0, weight=1)
    left_card.columnconfigure(1, weight=1)

    hdr_a = tk.Frame(left_card, bg=BORDER, pady=4); hdr_a.grid(row=0, column=0, sticky="ew")
    tk.Label(hdr_a, text="MATRIX A COEFFICIENTS", font=FONT_SMALL, bg=BORDER, fg=TEXT_DIM).pack(anchor="w", padx=10)
    
    hdr_b = tk.Frame(left_card, bg=BORDER, pady=4); hdr_b.grid(row=0, column=1, sticky="ew")
    tk.Label(hdr_b, text="MATRIX B COEFFICIENTS", font=FONT_SMALL, bg=BORDER, fg=TEXT_DIM).pack(anchor="w", padx=10)

    # Centered alignment wrapper panels
    wrapper_a = tk.Frame(left_card, bg=PANEL); wrapper_a.grid(row=1, column=0, sticky="nsew")
    wrapper_b = tk.Frame(left_card, bg=PANEL); wrapper_b.grid(row=1, column=1, sticky="nsew")

    grid_a_container = tk.Frame(wrapper_a, bg=PANEL); grid_a_container.pack(expand=True)
    grid_b_container = tk.Frame(wrapper_b, bg=PANEL); grid_b_container.pack(expand=True)

    # Right Container Card: Terminal Output Display Text Screen
    right_card = tk.Frame(workspace, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    right_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
    right_card.rowconfigure(1, weight=1)
    right_card.columnconfigure(0, weight=1)

    result_header = tk.Frame(right_card, bg=BORDER, pady=4)
    result_header.grid(row=0, column=0, sticky="ew")
    tk.Label(result_header, text="COMPUTATIONAL RESULTS RUNTIME REPORT", font=FONT_SMALL, bg=BORDER, fg=TEXT_DIM).pack(side="left", padx=12)

    output_display = tk.Text(right_card, font=("Courier New", 10), bg=ENTRY_BG, fg=TEXT, relief="solid", bd=1, wrap="none")
    output_display.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
    output_display.config(state="disabled")

    # ── GRID FACTORY GENERATOR ENGINE ───────────────────────────────────
    def build_grid(container, cells_list, rows, cols):
        for cell in cells_list: cell.destroy()
        cells_list.clear()

        for r in range(rows):
            for c in range(cols):
                cell = tk.Entry(container, font=FONT_MONO, justify="center", width=6,
                                bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
                                relief="solid", bd=1, highlightthickness=1,
                                highlightcolor=ACCENT, highlightbackground=BORDER)
                cell.grid(row=r, column=c, padx=4, pady=4, ipady=5)
                cell.insert(0, "0")
                cells_list.append(cell)

    def regenerate_all_grids(event=None):
        build_grid(grid_a_container, matrix_a_cells, int(r_a_var.get()), int(c_a_var.get()))
        build_grid(grid_b_container, matrix_b_cells, int(r_b_var.get()), int(c_b_var.get()))

    combo_ra.bind("<<ComboboxSelected>>", regenerate_all_grids)
    combo_ca.bind("<<ComboboxSelected>>", regenerate_all_grids)
    combo_rb.bind("<<ComboboxSelected>>", regenerate_all_grids)
    combo_cb.bind("<<ComboboxSelected>>", regenerate_all_grids)

    # ── COEFFICIENT DATA CAPTURE UTILITY ────────────────────────────────
    def _get_matrix(cells, rows, cols, matrix_name):
        vals = []
        for idx, cell in enumerate(cells):
            raw = cell.get().strip()
            if not raw: 
                raise ValueError(f"Empty input field found in {matrix_name} at position index #{idx+1}.")
            try:
                vals.append(float(raw))
            except ValueError:
                raise ValueError(f"Value '{raw}' found in {matrix_name} is non-numeric.")
        return np.array(vals).reshape(rows, cols)

    # ── CLEAR & STRUCTURED CONSOLE FORMATTER ─────────────────────────────
    def _print_success_report(title, res, dimensions_str):
        output_display.config(state="normal")
        output_display.delete("1.0", tk.END)
        
        output_display.insert(tk.END, f"┌────────────────────────────────────────────────────────┐\n")
        output_display.insert(tk.END, f"  OPERATION: {title.upper()}\n")
        output_display.insert(tk.END, f"  STATUS:    🟢 SUCCESSFUL COMPUTATION\n")
        output_display.insert(tk.END, f"  SHAPE:     {dimensions_str}\n")
        output_display.insert(tk.END, f"└────────────────────────────────────────────────────────┘\n\n")
        
        output_display.insert(tk.END, "OUTPUT VALUES:\n")
        if isinstance(res, (int, float, np.float64)):
            output_display.insert(tk.END, f"  👉 {res:,.6f}\n")
        elif len(res.shape) == 1:
            for i, val in enumerate(res):
                output_display.insert(tk.END, f"   Variable x{i+1} = {val:11.4f}\n")
        else:
            for row in res:
                row_str = "   ".join([f"{val:11.4f}" for val in row])
                output_display.insert(tk.END, f"   [  {row_str}  ]\n")
        output_display.config(state="disabled")

    def _print_error_report(title, error_message):
        output_display.config(state="normal")
        output_display.delete("1.0", tk.END)
        
        output_display.insert(tk.END, f"┌────────────────────────────────────────────────────────┐\n")
        output_display.insert(tk.END, f"  OPERATION: {title.upper()}\n")
        output_display.insert(tk.END, f"  STATUS:    ❌ INVALID DIMENSIONS / APPLICABILITY ERROR\n")
        output_display.insert(tk.END, f"└────────────────────────────────────────────────────────┘\n\n")
        output_display.insert(tk.END, f"MATHEMATICAL RULE ERROR:\n")
        output_display.insert(tk.END, f"⚠️ {error_message}\n")
        output_display.config(state="disabled")

    # ── EXECUTION & MATH GUARD LOGIC ──────────────────────────────────────
    def execute_calc(op):
        r_a, c_a = int(r_a_var.get()), int(c_a_var.get())
        r_b, c_b = int(r_b_var.get()), int(c_b_var.get())
        
        # 1. Handle Unary Matrix-A Operations
        if op in ["det", "inv", "trans", "pow", "adj", "solve"]:
            title_map = {
                "det": "Determinant |A|", 
                "inv": "Matrix Inverse A⁻¹", 
                "trans": "Transpose Aᵀ",
                "pow": f"Matrix Power A^{power_var.get()}",
                "adj": "Adjoint Matrix adj(A)",
                "solve": "System of Linear Equations (Ax = b)"
            }
            title = title_map[op]
            
            # System of Linear Equations Solver Guard via equations module
            if op == "solve":
                if c_a != r_a + 1:
                    _print_error_report(title, f"To solve a linear system, Matrix A must be formatted as an Augmented Matrix.\nExpected Columns = Rows + 1. Currently configured as ({r_a}x{c_a}).\n\n💡 Set Matrix A size to 2x3, 3x4, or 4x5 to use this feature.")
                    return
                try:
                    augmented = _get_matrix(matrix_a_cells, r_a, c_a, "Matrix A")
                    A_part = augmented[:, :-1]
                    b_part = augmented[:, -1]
                    
                    if determinant.determinant(A_part) == 0:
                        _print_error_report(title, "The coefficient subsystem has a determinant of 0. The system has zero or infinite solutions.")
                        return
                        
                    solution_vector = equations.solve_equations(A_part, b_part)
                    _print_success_report(title, solution_vector, f"{r_a} Variables Solved")
                except Exception as e:
                    show_error_popup(win, str(e))
                return

            # Square Shape Compatibility Check
            if op in ["det", "inv", "pow", "adj"] and r_a != c_a:
                _print_error_report(title, f"This operation requires a Square Matrix.\nYour Matrix A layout is currently non-square ({r_a}x{c_a}).")
                return
                
            try:
                A = _get_matrix(matrix_a_cells, r_a, c_a, "Matrix A")
                
                if op == "det":
                    _print_success_report(title, determinant.determinant(A), "Scalar Numerical Output")
                elif op == "inv":
                    if determinant.determinant(A) == 0:
                        _print_error_report(title, "This matrix is Singular (Determinant = 0) and cannot be inverted.")
                        return
                    _print_success_report(title, inverse.inverse_matrix(A), f"{r_a}x{c_a} Square Matrix")
                elif op == "trans":
                    _print_success_report(title, transpose.transpose_matrix(A), f"{c_a}x{r_a} Transposed Matrix")
                elif op == "pow":
                    k = int(power_var.get())
                    _print_success_report(title, power.power_matrix(A, k), f"{r_a}x{c_a} Raised Matrix")
                elif op == "adj":
                    if determinant.determinant(A) == 0:
                        _print_error_report(title, "Determinant is 0. Singular matrices cannot be processed through inverse adjoint methods safely.")
                        return
                    _print_success_report(title, adjoint.adjoint_matrix(A), f"{r_a}x{c_a} Adjoint Frame")
            except Exception as e:
                show_error_popup(win, str(e))

        # 2. Handle Binary Multi-Matrix Operations
        else:
            title_map = {
                "add": "Matrix Addition (A + B)",  
                "mul": "Matrix Multiplication (A × B)"
            }
            title = title_map[op]
            
            if op in ["add", "sub"] and ((r_a != r_b) or (c_a != c_b)):
                _print_error_report(title, f"Matrix addition requires matching dimensions.\nMatrix A is ({r_a}x{c_a}) while Matrix B is ({r_b}x{c_b}).")
                return
            if op == "mul" and c_a != r_b:
                _print_error_report(title, f"Inner dimensions must align: Matrix A Columns must equal Matrix B Rows.\nMatrix A Columns = {c_a}, but Matrix B Rows = {r_b}.")
                return
                
            try:
                A = _get_matrix(matrix_a_cells, r_a, c_a, "Matrix A")
                B = _get_matrix(matrix_b_cells, r_b, c_b, "Matrix B")
                
                if op == "add":
                    _print_success_report(title, addition.matrix_addition(A, B), f"{r_a}x{c_a} Matrix")
                elif op == "mul":
                    _print_success_report(title, multiplication.matrix_multiplication(A, B), f"{r_a}x{c_b} Computed Matrix")
            except Exception as e:
                show_error_popup(win, str(e))

    # ── EXPANDED INTERFACE CONTROL BUTTONS ───────────────────────────────
    action_panel = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    action_panel.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
    action_panel.columnconfigure(0, weight=6)
    action_panel.columnconfigure(1, weight=4)

    # Section 1: Matrix A Evaluation Options
    f1 = tk.LabelFrame(action_panel, text=" Operations on Matrix A ", font=FONT_SMALL_FIXED, bg=PANEL, fg=TEXT_DIM, padx=8, pady=8)
    f1.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=8)
    f1.rowconfigure(0, weight=1) 
    for col_idx in range(6): f1.columnconfigure(col_idx, weight=1)
    
    b_det = StyledButton(f1, "Determinant |A|", lambda: execute_calc("det"), color="#2563eb")
    b_det.grid(row=0, column=0, sticky="nsew", padx=3, ipady=12)
    
    b_inv = StyledButton(f1, "Inverse A⁻¹", lambda: execute_calc("inv"), color="#2563eb")
    b_inv.grid(row=0, column=1, sticky="nsew", padx=3, ipady=12)
    
    b_trn = StyledButton(f1, "Transpose Aᵀ", lambda: execute_calc("trans"), color="#475569")
    b_trn.grid(row=0, column=2, sticky="nsew", padx=3, ipady=12)

    b_pow = StyledButton(f1, "Power Aᵏ", lambda: execute_calc("pow"), color="#6366f1")
    b_pow.grid(row=0, column=3, sticky="nsew", padx=3, ipady=12)

    b_adj = StyledButton(f1, "Adjoint adj(A)", lambda: execute_calc("adj"), color="#3b82f6")
    b_adj.grid(row=0, column=4, sticky="nsew", padx=3, ipady=12)

    b_slv = StyledButton(f1, "Solve System Ax=b", lambda: execute_calc("solve"), color="#f97316")
    b_slv.grid(row=0, column=5, sticky="nsew", padx=3, ipady=12)

    # Section 2: Dual Matrix Evaluation Options
    f2 = tk.LabelFrame(action_panel, text=" Dual Matrix Operations ", font=FONT_SMALL_FIXED, bg=PANEL, fg=TEXT_DIM, padx=8, pady=8)
    f2.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=8)
    f2.rowconfigure(0, weight=1) 
    for col_idx in range(4): f2.columnconfigure(col_idx, weight=1)
    
    b_add = StyledButton(f2, "Addition (A+B)", lambda: execute_calc("add"), color="#10b981")
    b_add.grid(row=0, column=0, sticky="nsew", padx=3, ipady=12)
    
    b_mul = StyledButton(f2, "Multiplication (A×B)", lambda: execute_calc("mul"), color="#d97706")
    b_mul.grid(row=0, column=2, sticky="nsew", padx=3, ipady=12)

    b_rst = StyledButton(f2, "Reset Fields", lambda: regenerate_all_grids(), color="#64748b")
    b_rst.grid(row=0, column=3, sticky="nsew", padx=3, ipady=12)

    # Initialize input grids on application startup
    regenerate_all_grids()
    return build