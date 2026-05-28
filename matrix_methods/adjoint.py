import numpy as np

def adjoint_matrix(A):

    det = np.linalg.det(A)

    inv = np.linalg.inv(A)

    return det * inv