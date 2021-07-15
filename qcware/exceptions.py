class QCWareClientException(Exception):
    pass


class ApiException(QCWareClientException):
    pass


class ApiCallFailedError(ApiException):
    pass


class ApiCallResultUnavailableError(ApiException):
    pass


class ApiCallExecutionError(ApiException):
    def __init__(self, message, traceback, api_call_info=dict()):
        super().__init__(message)
        self.traceback = traceback
        self.api_call_info = api_call_info


class ApiTimeoutError(ApiException):
    def __init__(self, api_call_info, message=None):
        if message is None:
            message = f"""API Call timed out.
You can retrieve with qcware.api_calls.retrieve_result(call_token='{api_call_info['uid']}')
or use the .submit or .call_async forms of the API call.
See the getting started notebook "Retrieving_long_task_results.ipynb" in Forge"""
        super().__init__(message)
        self.api_call_info = api_call_info
