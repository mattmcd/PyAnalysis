from __future__ import division
import numpy as np

"""Lattice reduction algorithms
Code from 'Lattice Reduction: A survey with applications in wireless
communications', Wubben, Seethaler, Jalden and Matz
IEE Signal Processing Magazine (70) May 2011
and references therein.
"""

def sorted_qr(A):
    """Sorted QR decomposition following Wubben 2001
    Performs a QR decomposition with permutation such that the
    diagonal elements of R are decreasing.
    One use of this is in Lattice Reduction using the LLL algorithm
    as it reduces the processing requried.

    Parameters
    ----------
    A - square matrix

    Returns
    -------
    Q - matrix of orthogonal vectors
    R - upper triangular matrix with increasing diagonal elements
    p - column permutation vector such that
        np.dot(Q, )[:, ] == A
    """
    nCols = np.size(A, 1)
    Q = A.copy()
    R = np.zeros((Q.shape[1],Q.shape[1])) # nCols x nCols
    p = np.arange(nCols)
    for i in range(nCols):
        # Find column with minimum norm
        minInd = i + np.argsort(np.sqrt(sum(Q[:, i:]**2, 0)))[0]
        # Swap columns i and minInd
        p[[i, minInd]] = p[[minInd, i]]
        Q[:, [i, minInd]] = Q[:, [minInd, i]]
        R[:, [i, minInd]] = R[:, [minInd, i]]
        # Normal Gram-Schmidt process
        R[i, i] = np.linalg.norm(Q[:, i])
        Q[:, i] = Q[:, i] / R[i, i]
        for j in range(i+1, nCols):
            R[i, j] = np.dot(Q[:, i], Q[:, j])
            Q[:, j] = Q[:, j] - R[i, j]*Q[:, i]
    return Q, R, p


def lattice_reduce(A, delta=0.75):
    """Lenstra-Lenstra-Lovasz (LLL) reduction
    Find short basis vectors for a given matrix

    Parameters
    ----------
    A - basis matrix
    delta - reduction parameter, default 0.75

    Returns
    -------
    A_ - reduced basis matrix
    T - unimodular matrix such that A_ = AT
    """

    Q, R, p = sorted_qr(A)
    m = A.shape[1]
    T = np.eye(m)[:, p]
    k = 1

    while k < m:
        for i in reversed(range(0, k)):
            mu = round(R[i, k]/R[i, i])
            if mu != 0:
                R[0:i+1, k] = R[0:i+1, k] - mu*R[0:i+1, i]
                T[:, k] = T[:, k] - mu*T[:, i]
        defect = delta*R[k-1, k-1]**2 > R[k, k]**2 - mu*R[k-1, k]**2
        if defect:
            # Swap columns k-1 and k in R and T
            R[:, [k, k-1]] = R[:, [k-1, k]]
            T[:, [k, k-1]] = T[:, [k-1, k]]
            # Givens rotation
            a = R[k-1, k-1]/np.linalg.norm(R[k-1:k+1, k-1])
            b = R[k, k-1]/np.linalg.norm(R[k-1:k+1, k-1])
            theta = np.array([[a, b], [-b, a]])
            R[k-1:k+1, k-1:m+1] = theta.dot(R[k-1:k+1, k-1:m+1])
            Q[:, k-1:k+1] = Q[:, k-1:k+1].dot(theta.T)
        else:
            k += 1

    B_ = Q.dot(R)
    return B_, T


def lattice_det(A):
    """Lattice determinant of a m x n matrix
    Calculates L = sqrt(det(B.T.dot(B)))
    """
    
    return np.sqrt(np.linalg.det(A.T.dot(A)))


def orth_defect(A):
    """Orthogonality defect of m x n matrix
    Equal to product of the column norms divided by lattice determinant.
    """
    
    col_norms = map(np.linalg.norm, A.T)
    return np.prod(col_norms) / lattice_det(A)
