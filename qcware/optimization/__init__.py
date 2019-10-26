"""optimization.

The module for interfacing with QC Ware's optimization library and
platform solvers.

"""

from . import utils

from ._qubo import *
from ._ising import *
from ._pubo import *
from ._hising import *
from ._hobo import *
from ._hoio import *
from ._solve_binary import *

from ._qubo import __all__ as __all_qubo__
from ._ising import __all__ as __all_ising__
from ._pubo import __all__ as __all_pubo__
from ._hising import __all__ as __all_hising__
from ._hobo import __all__ as __all_hobo__
from ._hoio import __all__ as __all_hoio__
from ._solve_binary import __all__ as __all_sb__

__all__ = (
    __all_qubo__ +
    __all_ising__ +
    __all_pubo__ +
    __all_hising__ +
    __all_hobo__ +
    __all_hoio__ +
    __all_sb__
)

from . import sat
from . import problems

name = "qcware"
