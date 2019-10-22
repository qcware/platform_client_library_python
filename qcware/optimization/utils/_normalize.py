"""_normalize.py.

This file contains the function to normalize QUBOs, PUBOs, Isings,
HIsings, etc.

"""

import numpy as np


__all__ = 'normalize',


def normalize(D, value=1):
    """normalize.

    Normalize the coefficients to a maximum magnitude.

    Parameters
    ----------
    D : dict or subclass of dict.
    value : float (optional, defaults to 1).
        Every coefficient value will be normalized such that the
        coefficient with the maximum magnitude will be +/- 1.

    Return
    ------
    res : same as type(D).
        ``D`` but with coefficients that are normalized to be within +/- value.

    Examples
    --------
    >>> from qcware.optimization.utils import DictArithmetic, normalize
    >>> d = {(0, 1): 1, (1, 2, 'x'): 4}
    >>> print(normalize(d))
    {(0, 1): 0.25, (1, 2, 'x'): 1}

    >>> from qcware.optimization.utils import DictArithmetic, normalize
    >>> d = {(0, 1): 1, (1, 2, 'x'): -4}
    >>> print(normalize(d))
    {(0, 1): 0.25, (1, 2, 'x'): -1}

    >>> from qcware.optimization import PUBO
    >>> d = PUBO({(0, 1): 1, (1, 2, 'x'): 4})
    >>> print(normalize(d))
    {(0, 1): 0.25, (1, 2, 'x'): 1}

    >>> from qcware.optimization.utils import PUBO
    >>> d = PUBO({(0, 1): 1, (1, 2, 'x'): -4})
    >>> print(normalize(d))
    {(0, 1): 0.25, (1, 2, 'x'): -1}


    """
    res = type(D)()
    mult = value / max(abs(v) for v in D.values())
    for k, v in D.items():
        res[k] = mult * v
    return res
