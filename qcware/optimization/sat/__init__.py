"""``sat`` is a module for converting SAT problems into QUBO/Ising form.

``sat`` is a library of ``qcware.optimization`` for converting satisfiability problems
into PUBOs (see ``help(qcware.optimization.PUBO)``).

"""

from ._satisfiability import *

from ._satisfiability import __all__ as __all_sat__

__all__ = (
    __all_sat__
)

name = "sat"
