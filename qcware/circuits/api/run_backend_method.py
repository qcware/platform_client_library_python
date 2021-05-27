#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import asyncio
import warnings
from ...api_calls import declare_api_call


@declare_api_call(name="circuits.run_backend_method",
                  endpoint="circuits/run_backend_method")
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
:rtype: object
"""
    pass


def submit_run_backend_method(*args, **kwargs):
    """This method is deprecated; please use run_backend_method.submit"""
    w = "The old submit_run_backend_method function has been deprecated and will be removed.  Please use run_backend_method.submit"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return run_backend_method.submit(*args, **kwargs)


async def async_run_backend_method(*args, **kwargs):
    """This method is deprecated; please use run_backend_method.call_async"""
    w = "The old async_run_backend_method function has been deprecated and will be removed.  Please use run_backend_method.call_async"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return await run_backend_method.call_async(*args, **kwargs)
