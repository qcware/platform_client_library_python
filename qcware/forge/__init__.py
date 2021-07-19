#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


"""
This is the client library for QC Ware's Forge product,
a SaaS product for solving problems with quantum computing.
Please see the documentation at http://qcware.readthedocs.io
"""
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("qcware").version
except Exception:
    __version__ = "5.3.2"

import logging

logger = logging.getLogger("qcware")


from . import qio
from . import qutils
from . import circuits
from . import qml
from . import test
from . import optimization
