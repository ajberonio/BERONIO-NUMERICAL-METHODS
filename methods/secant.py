# methods/secant.py
# Columns (from docx): Iteration Number | Xi-1 | Xi | Xi+1 | |Ea|,% | f(Xi-1) | f(Xi) | f(Xi+1)
# Iteration 1 has no Ea (blank) — no previous Xi+1 to compare

def secant(f, x0, x1, tol):
    """
    Secant Method.
    x0 = Xi-1 (Xl input)  — first initial guess
    x1 = Xi   (Xu input)  — second initial guess
    tol = stopping tolerance as a percentage (es)

    Row format: (Iteration Number, Xi-1, Xi, Xi+1, |Ea|,%, f(Xi-1), f(Xi), f(Xi+1))
    Iteration 1 has Ea blank (no previous Xi+1).
    """
    iterations = []
    i          = 1
    xi1_old    = None

    while True:
        fx0 = f(x0)
        fx1 = f(x1)

        if (fx0 - fx1) == 0:
            raise Exception(
                "Division by zero in secant formula.\n"
                "f(Xi-1) equals f(Xi) — the secant line is horizontal.\n"
                "Try different initial guesses.")

        # Secant formula
        xi1  = x1 - (fx1 * (x0 - x1)) / (fx0 - fx1)
        fxi1 = f(xi1)

        # Ea blank for first iteration
        if xi1_old is None:
            ea = ""
        else:
            ea = abs((xi1 - xi1_old) / xi1) * 100 if xi1 != 0 else 0.0

        iterations.append([
            i,                                         # Iteration Number
            round(x0,   6),                            # Xi-1
            round(x1,   6),                            # Xi
            round(xi1,  6),                            # Xi+1
            "" if ea == "" else round(ea, 6),          # |Ea|,%
            round(fx0,  6),                            # f(Xi-1)
            round(fx1,  6),                            # f(Xi)
            round(fxi1, 6),                            # f(Xi+1)
        ])

        if ea != "" and ea < tol:
            break
        if abs(fxi1) < 1e-10:
            break
        if i >= 100:
            break

        x0      = x1
        x1      = xi1
        xi1_old = xi1
        i      += 1

    return xi1, iterations