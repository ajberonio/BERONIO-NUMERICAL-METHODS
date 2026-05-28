# methods/false_position.py
# Columns: Iteration | XL | XU | XR | Ea | f(XL) | f(XU) | f(XR) | f(XL)*f(XR)
# Remarks from PDF:
#   f(XL)*f(XR) < 0  → "xR = xU"  (root between XL and XR, set XU = XR)
#   f(XL)*f(XR) > 0  → "xR = xL"  (root between XR and XU, set XL = XR)
#   f(XL)*f(XR) = 0  → "Root found (exact)"

def false_position(f, xl, xu, tol):

    if f(xl) * f(xu) > 0:
        raise ValueError(
            "f(XL) and f(XU) have the same sign.\n"
            "The function must change sign between XL and XU.\n"
            "Try different values for Xl and Xu.")

    iterations = []
    xr_old     = None

    for i in range(1, 101):

        fxl = f(xl)
        fxu = f(xu)

        xr   = xu - (fxu * (xl - xu)) / (fxl - fxu)
        fxr  = f(xr)
        test = fxl * fxr

        if xr_old is None:
            ea = ""
        else:
            ea = abs((xr - xr_old) / xr) * 100 if xr != 0 else 0.0

        if test < 0:
            remark = "xR = xU"
            xu = xr
        elif test > 0:
            remark = "xR = xL"
            xl = xr
        else:
            remark = "Root found (exact)"

        iterations.append([
            i,
            round(xl,   6),
            round(xu,   6),
            round(xr,   6),
            "" if ea == "" else round(ea, 6),
            round(fxl,  6),
            round(fxu,  6),
            round(fxr,  6),
            round(test, 6),
        ])

        if remark == "Root found (exact)":
            break
        if ea != "" and ea < tol:
            break
        if abs(fxr) < 1e-10:
            break

        xr_old = xr

    return xr, iterations