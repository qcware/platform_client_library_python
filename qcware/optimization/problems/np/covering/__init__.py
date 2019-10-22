"""``covering`` contains many NP covering problems.

Here we have the QUBO/Ising conversions for common covering problems.
The conversions are based on [Lucas].

References
----------
.. [Lucas] Andrew Lucas. Ising formulations of many np problems. Frontiers in
    Physics, 2:5, 2014.

"""

from ._set_cover import *
from ._vertex_cover import *

from ._set_cover import __all__ as __all_sc__
from ._vertex_cover import __all__ as __all_vc__

__all__ = (
    __all_sc__ +
    __all_vc__
)

name = "covering"
