"""``coloring`` contains many NP coloring problems.

Here we have the QUBO/Ising conversions for common coloring probems,
The conversions are based on [Lucas].

References
----------
.. [Lucas] Andrew Lucas. Ising formulations of many np problems. Frontiers in
    Physics, 2:5, 2014.

"""

from ._job_sequencing import *

from ._job_sequencing import __all__ as __all_js__

__all__ = (
    __all_js__
)

name = "coloring"
