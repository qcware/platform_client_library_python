"""``problems`` contains many problems converted to QUBO/Ising form.

This module contains many all the problems that we convert to QUBO/Ising form.
We organize all the problems into categories, but we import them globally for
user use. See the ``__all__`` value for all the problems imported. Each of the
problems inherits from the ``Problem`` parent class, see
``qcware.optimization.problems.Problem``.

"""

from ._problem_parentclass import *  # don't add to __all__!

from .np import *
from .benchmarking import *

from .np import __all__ as __all_np__
from .benchmarking import __all__ as __all_benchmarking__

__all__ = (
    __all_np__ + __all_benchmarking__
)

name = "problems"
