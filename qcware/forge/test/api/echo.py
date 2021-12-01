#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(name="test.echo", endpoint="test/echo")
def echo(text: str = "hello world."):
    r"""

    Arguments:

    :param text: The text to return, defaults to hello world.
    :type text: str


    :return:
    :rtype:"""
    pass
