#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(
    name="circuits.run_backend_method", endpoint="circuits/run_backend_method"
)
def run_backend_method(backend: str, method: str, kwargs: dict):
    r"""Runs an arbitrary backend method.  This API call is not intended to be used directly by users; rather, it is meant to be called by the QuasarBackend class to transparently delegate class method calls to Forge API endpoints.

    Arguments:

    :param backend: string representing the backend
    :type backend: str

    :param method: name of the method to be called
    :type method: str

    :param kwargs: Keyword args passed to the method.  Positional args should be converted to kwargs
    :type kwargs: dict


    :return: variable; see Quasar documentation
    :rtype: object"""
    pass
