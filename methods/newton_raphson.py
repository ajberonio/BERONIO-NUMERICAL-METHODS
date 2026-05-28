# methods/newton_raphson.py
# Columns (from PDF): No. of Iteration | Xi | |Ea|,% | f(Xi) | f'(Xi)
# Note: iteration 0 has no Ea (blank) — it is the initial value row
# Xi+1 is computed but shown in the NEXT row as Xi

def derivative(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


def newton_raphson(f, x0, tol):
    """
    Newton-Raphson Method.
    x0  = initial guess (Xl input)
    tol = stopping tolerance as a percentage (es)

    Row format: (No. of Iteration, Xi, |Ea|,%, f(Xi), f'(Xi))
    Iteration 0 = initial value row, Ea is blank.
    """
    iterations = []

    xi = x0

    for i in range(0, 51):

        fxi  = f(xi)
        dfxi = derivative(f, xi)

        if dfxi == 0:
            raise Exception(
                f"Derivative is zero at Xi = {xi:.6f}.\n"
                "Newton-Raphson cannot continue.\n"
                "Try a different initial guess (Xl).")

        xi1 = xi - fxi / dfxi

        # Ea is blank for iteration 0 (no previous value)
        if i == 0:
            ea = ""
        else:
            ea = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else 0.0

        iterations.append([
            i,                                        # No. of Iteration
            round(xi,   6),                           # Xi
            "" if ea == "" else round(ea, 6),         # |Ea|,%
            round(fxi,  6),                           # f(Xi)
            round(dfxi, 6),                           # f'(Xi)
        ])

        # Stop after computing ea (i >= 1) when tolerance is met
        if i >= 1 and ea != "" and ea < tol:
            break
        if abs(fxi) < 1e-10:
            break
        if i >= 50:
            break

        xi = xi1

    return xi1, iterations