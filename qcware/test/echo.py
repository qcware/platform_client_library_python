#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
  


def echo(text:str='hello world.', api_key:str=None, host:str=None):
    r"""

Arguments:

:param text: , defaults to hello world.
:type text: str


:return: 
:rtype: 
    """
    data = client_args_to_wire('test.echo', **locals())
    api_call = post_call('test/echo', data, host=host )
    logger.info(f'API call to test.echo successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))
