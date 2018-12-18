from functools import wraps
import warnings
from qcware.version import version_is_greater, parameter_api_version


def print_errors(f):
    """
    If the result returned by f (presumably an API call)
    contains an error code, print a warning that an error occurred
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, dict):
            if "error_code" in result:
                msg = "Error: {0} (code: {1})".format(
                    result["error"], result["error_code"]
                )
                warnings.warn(msg, stacklevel=3)
            elif "error" in result and "exception_type" in result:
                msg = "{0}; examine result for traceback".format(
                    result["error"]
                )
                warnings.warn(msg, stacklevel=3)
        return result

    return decorated


def print_api_mismatch(f):
    """
    If the result returned by f contains an 'api_version' string,
    compare that to the internal one.  If the result's version is
    higher (meaning that the server has a higher api version than the
    client) print a deprecation warning.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, dict) and "api_version" in result:
            if version_is_greater(result['api_version']):
                msg = "Older API: your version: {0}; server: {1}.  Consider upgrading with `pip install --upgrade qcware`".format(
                    parameter_api_version(),
                    result['api_version']
                )
                warnings.warn(msg, stacklevel=2)
        return result

    return decorated
