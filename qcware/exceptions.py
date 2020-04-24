class QCWareClientException(Exception):
    pass


class ApiException(QCWareClientException):
    pass


class ApiCallFailedError(ApiException):
    pass


class ApiCallExecutionError(ApiException):
    pass
