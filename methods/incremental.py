# methods/incremental.py

def incremental(f, xl, xu, step=0.5):

    iterations = []
    i = 1

    while True:

        x_next = xl + step

        fxl = f(xl)
        fxu = f(x_next)

        dx = step
        prod = fxl * fxu

        # -------------------------
        # REMARK
        # -------------------------
        if prod < 0:
            remark = "<0 Revert back to xl & consider smaller interval"
        else:
            remark = ">0 Go to next interval"

        # -------------------------
        # STORE ITERATION
        # -------------------------
        iterations.append([
            i,
            round(xl, 6),
            round(dx, 6),
            round(x_next, 6),
            round(fxl, 6),
            round(fxu, 6),
            round(prod, 6),
            remark
        ])

        # -------------------------
        # CONDITIONS
        # -------------------------
        if fxl == 0:
            root = xl
            return root, iterations

        elif fxu == 0:
            root = x_next
            return root, iterations

        elif prod < 0:
            # revert and refine
            xu = x_next
            step = step / 2

        else:
            # move forward
            xl = x_next

        # -------------------------
        # STOP CONDITIONS
        # -------------------------
        if step < 1e-4:
            root = xl
            return root, iterations

        if i > 100:
            root = xl
            return root, iterations

        i += 1