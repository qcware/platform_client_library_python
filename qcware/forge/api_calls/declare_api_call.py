import inspect

from qcware.forge.config import client_timeout
from qcware.forge.exceptions import ApiTimeoutError
from qcware.serialization.transforms import client_args_to_wire

from qcware.forge import logger
from qcware.forge.api_calls.api_call import (
    async_post_call,
    async_retrieve_result,
    handle_result,
    post_call,
    wait_for_call,
)


class ApiCall:
    def __call__(self, *args, **kwargs):
        return self.do(*args, **kwargs)

    def data(self, *args, **kwargs):
        new_bound_kwargs = self.__signature__.bind(*args, **kwargs)
        new_bound_kwargs.apply_defaults()
        new_kwargs = new_bound_kwargs.arguments
        return client_args_to_wire(self.name, **new_kwargs)

    def do(self, *args, **kwargs):
        api_call = post_call(self.endpoint, self.data(*args, **kwargs))
        api_call_id = api_call["uid"]
        logger.info(
            f"API call to {self.name} successful; api call token is {api_call_id}"
        )
        if client_timeout() == 0:
            raise ApiTimeoutError(api_call)
        else:
            return handle_result(wait_for_call(call_token=api_call_id))

    def submit(self, *args, **kwargs):
        api_call = post_call(self.endpoint, self.data(*args, **kwargs))
        logger.info(
            f'Call submitted to {self.name} successful; api call token is {api_call["uid"]}'
        )
        return api_call["uid"]

    async def call_async(self, *args, **kwargs):
        api_call = await async_post_call(self.endpoint, self.data(*args, **kwargs))
        logger.info(
            f'Async call to {self.name} successful; api call token is {api_call["uid"]}'
        )
        return await async_retrieve_result(api_call["uid"])


# much of this is inspired by the celery task decorator;
# see https://github.com/celery/celery/blob/8d6778810c5153c9e4667eed618de2d0bf72663e/celery/app/base.py#L452
def declare_api_call(name, endpoint):
    def inner_decorator(f):
        result = type(
            f.__name__,
            (ApiCall,),
            dict(
                {
                    "name": name,
                    "endpoint": endpoint,
                    "_decorated": True,
                    "__doc__": f.__doc__,
                    "__module__": f.__module__,
                    "__annotations__": f.__annotations__,
                    "__signature__": inspect.signature(f),
                    "__wrapper__": f,
                }
            ),
        )()

        return result

    return inner_decorator
