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


def convert_solutions(f):
    """Maps solution outputs from `solve_binary` to the form that they were inputted.

    See `_recursively_convert_solutions` for more info.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        _recursively_convert_solutions(result)
        return result

    return decorated


def _recursively_convert_solutions(result, mapping=None):
    r"""Convert solutions with their enumeration.

    The output of the request to `solve_binary` is a dictionary with various
    keys. `mapping` is a `dict` that maps indicies of the solutions lists to
    the keys that the user originally used in their QUBO `dict`. This
    function recursively goes through the result and converts all solution
    lists to a dictionary that maps the user's original keys to the correct
    values. Note that the `result` dictionary is modified in place!

    Args:
        result (:obj:`dict`): The output of `qcware.optimization.solve_binary`.
        mapping (:obj:`dict`): Dictionary that maps integer indices used in the QUBO to the user's original inputs.
            If `mapping` is not provided, then we look for a key `enumeration` in `result`.

    Returns:
        None. The `result` dictionary is modified in place.
    """
    if mapping is None:
        if "enumeration" not in result:
            return
        mapping = result["enumeration"]

    # through recursive calls
    if isinstance(result, list):
        try:
            return {mapping[i]: int(v) for i, v in enumerate(result)}
        except (KeyError, TypeError):
            return [_recursively_convert_solutions(x, mapping) for x in result]

    elif isinstance(result, dict):
        for k, v in tuple(result.items()):
            if isinstance(v, dict):
                _recursively_convert_solutions(v, mapping)
            elif k in ("solution", "all_solutions", "unique_solutions"):
                result[k] = _recursively_convert_solutions(v, mapping)
