# This shim is in place only to serve as a warning that the old "qcware" package
# is now a namespace package and the forge client now lives under
# qcware.forge
import warnings

warnings.warn(
    """
The forge client has been reorganized under qcware.forge; for
every case where you would "import qcware" you should replace this
with "from qcware import forge" and then use "forge.optimization..."
"forge.qml..." etc.  Currently the old functionality is shimmed
into the "qcware" namespace, but this compatibility will be removed
in a future version.
""",
    FutureWarning,
)

from .forge import *
