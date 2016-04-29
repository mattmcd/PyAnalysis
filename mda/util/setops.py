from __future__ import division
import numpy as np


def remove_duplicates(lst):
    """Remove duplicates from a list"""
    (els, inds) = np.unique(lst, return_index=True)
    out = np.zeros(lst.shape, dtype=lst.dtype)
    out[inds] = els
    return out
