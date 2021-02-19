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
    def __init__(self, message, api_call_info):
        super().__init__(message)
        self.api_call_info = api_call_info
