import numpy as np

def sortedQR(A):
  """Sorted QR decomposition following Wubben 2001
     Performs a QR decomposition with permutation such that the 
     diagonal elements of R are decreasing.  
     One use of this is in Lattice Reduction using the LLL algorithm
     as it reduces the processing requried.
  """
  nCols = np.size(A,1)
  Q = A.copy()
  R = np.zeros((np.size(Q,1),np.size(Q,1)))
  p = np.arange(nCols)
  for i in range(nCols):
    # Find column with minimum norm
    minInd = i+np.argsort( np.sqrt( sum(Q[:,i:]**2,0)))[0]
    # Swap columns i and minInd
    p[[i,minInd]] = p[[minInd,i]]
    Q[:,[i,minInd]] = Q[:,[minInd,i]]
    R[:,[i,minInd]] = R[:,[minInd,i]]
    # Normal Gram-Schmidt process
    R[i,i] = np.linalg.norm(Q[:,i])
    Q[:,i] = Q[:,i] / R[i,i]
    for j in range(i+1,nCols):
      R[i,j] = np.dot(Q[:,i], Q[:,j])
      Q[:,j] = Q[:,j] - R[i,j]*Q[:,i]
  return Q,R,p
