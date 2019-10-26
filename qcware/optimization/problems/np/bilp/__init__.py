"""``bilp`` contains common Binary Linear Integer Programming problems.

Here we have the QUBO/Ising conversions for common binary integer
linear programming probems. The conversions are based on [Lucas]_.

References
----------
.. [Lucas] Andrew Lucas. Ising formulations of many np problems. Frontiers in
    Physics, 2:5, 2014.

"""

from ._bilp import *

from ._bilp import __all__ as __all_bilp__

__all__ = (
    __all_bilp__
)

name = "bilp"
