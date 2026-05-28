# methods/bisection.py

def bisection(f, xl, xu, tol):

    # -------------------------
    # INITIAL SIGN CHECK
    # -------------------------
    if f(xl) * f(xu) > 0:
        raise ValueError(
            "No sign change. Choose different xl and xu."
        )

    table = []

    i = 1
    ea = 100
    xr_old = 0

    while ea > tol:

        xr = (xl + xu) / 2

        fxl = f(xl)
        fxr = f(xr)

        test = fxl * fxr

        # -------------------------
        # COMPUTE ERROR
        # -------------------------
        if i > 1:
            if xr != 0:
                ea = abs((xr - xr_old) / xr) * 100
            else:
                ea = 0

        # -------------------------
        # CONDITIONS + REMARKS
        # -------------------------
        if fxr == 0:

            remark = "Exact Root"

            # store before exit
            table.append([
                i,
                round(xl, 6),
                round(xr, 6),
                round(xu, 6),
                round(fxl, 6),
                round(fxr, 6),
                round(ea, 6),
                round(test, 6),
                remark
            ])

            root = xr
            return root, table

        elif test < 0:
            remark = "<0 1st subinterval (xu = xr)"

        else:
            remark = ">0 2nd subinterval (xl = xr)"

        # -------------------------
        # STORE
        # -------------------------
        table.append([
            i,
            round(xl, 6),
            round(xr, 6),
            round(xu, 6),
            round(fxl, 6),
            round(fxr, 6),
            round(ea, 6),
            round(test, 6),
            remark
        ])

        # -------------------------
        # UPDATE BOUNDS
        # -------------------------
        if test < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr
        i += 1

        # safety stop
        if i > 100:
            break

    root = xr

    return root, table