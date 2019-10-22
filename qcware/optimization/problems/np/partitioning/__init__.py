"""``partitioning`` contains many NP partitioning problems.

Here we have the QUBO/Ising conversions for common partitioning probems,
The conversions are based on [Lucas].

References
----------
.. [Lucas] Andrew Lucas. Ising formulations of many np problems. Frontiers in
   Physics, 2:5, 2014.

"""

from ._number_partitioning import *
from ._graph_partitioning import *

from ._number_partitioning import __all__ as __all_np__
from ._graph_partitioning import __all__ as __all_gp__

__all__ = (
    __all_np__ +
    __all_gp__
)

name = "partitioning"
