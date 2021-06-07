#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import warnings
from ...api_calls import declare_api_call


@declare_api_call(name="test.echo", endpoint="test/echo")
def echo(text: str = 'hello world.'):
    r"""

Arguments:

:param text: The text to return, defaults to hello world.
:type text: str

  
:return: 
:rtype: 
"""
    pass


def submit_echo(*args, **kwargs):
    """This method is deprecated; please use echo.submit"""
    w = "The old submit_echo function has been deprecated and will be removed.  Please use echo.submit"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return echo.submit(*args, **kwargs)


async def async_echo(*args, **kwargs):
    """This method is deprecated; please use echo.call_async"""
    w = "The old async_echo function has been deprecated and will be removed.  Please use echo.call_async"
    warnings.warn(w, DeprecationWarning)
    print(w)
    return await echo.call_async(*args, **kwargs)
