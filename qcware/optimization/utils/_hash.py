"""_hash.py.

This file contains the hash function that we use to sort keys in the matrices,
used in PUBOMatrix, HIsingMatrix, QUBOMatrix, IsingMatrix, and all of their
subclasses.

"""

__all__ = 'hash_function',


def hash_function(x):
    """hash_function.

    Function to return (usually) unique hashes for ``x`` such
    that multiple ``x`` s can be ordered. Note that the hash is not consistent
    across Python sessions (except for when ``x`` is an integer)!

    Parameters
    ----------
    x : hashable object.

    Returns
    -------
    res : int.
        If ``x`` is an integer, then ``res == x``. Otherwise,
        ``res == hash(x)``.

    """
    return x if isinstance(x, int) else hash(x)
