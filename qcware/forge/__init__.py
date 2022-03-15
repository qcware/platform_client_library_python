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
    __version__ = "7.4.1"

import logging

logger = logging.getLogger("qcware.forge")


from qcware.forge import qio
from qcware.forge import montecarlo
from qcware.forge import qutils
from qcware.forge import circuits
from qcware.forge import qml
from qcware.forge import test
from qcware.forge import optimization
