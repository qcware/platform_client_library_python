from decouple import config, UndefinedValueError
from urllib.parse import urlparse
from typing import Optional
import os


class ConfigurationError(Exception):
    pass


def qcware_api_key(override: Optional[str] = None) -> str:
    """
    Returns the API key from environment variable QCWARE_API_KEY, config file,
    or the provided override (if the override is provided, this function simply
    returns the provided override)
    """
    try:
        result = override if override is not None else config('QCWARE_API_KEY')
    except UndefinedValueError:
        raise ConfigurationError("You have not provided a QCWare API key.  "
                                 "Please set one with the argument api_key, "
                                 "by calling qcware.set_api_key, or via "
                                 "configuration variables or files.")
    return result


def is_valid_host_url(url: str) -> bool:
    """
    Checks if a host url is valid.  A valid host url is just a scheme
    (http/https), a net location, and no path.
    """
    result = urlparse(url)
    return all([result.scheme, result.netloc]) and not result.path


def qcware_host(override: Optional[str] = None) -> str:
    """
    Returns the QCWare host url from the environment variable QCWARE_HOST,
    a config file, or the provided override.  The url should be in the form
    'scheme://netloc' where scheme is http or https and netloc is the
    IP address or name of the host.  No trailing slash is required
    (or desired).

    If an override is provided, this function checks for validity and returns
    the override.
    """
    # get the host; default is https://api.forge.qcware.com; this should
    # always work
    result = override if override is not None \
        else config('QCWARE_HOST', 'https://api.forge.qcware.com')
    # check to make sure the host is a valid url

    if is_valid_host_url(result):
        return result
    else:
        raise ConfigurationError(
            f"Configured QCWARE_HOST ({result}): does not seem to be"
            "a valid URL.  Please select a host url with scheme"
            "(http or https) and no path, e.g."
            "'http://api.forge.qcware.com'")


def set_api_key(key: str):
    """
    Set's the user's forge API key via environment variable.
    Equivalent to os.environ['QCWARE_API_KEY']=key
    """
    os.environ['QCWARE_API_KEY'] = key


def set_host(host_url: str):
    if is_valid_host_url(host_url):
        os.environ['QCWARE_HOST'] = host_url
    else:
        raise ConfigurationError(
            f"Requested QCWARE_HOST ({host_url}): does not"
            " seem to be a valid URL.  Please select a host url"
            "with scheme (http or https) and no path, e.g."
            "'http://api.forge.qcware.com'")


def max_wait_in_seconds(override: Optional[int] = None):
    """
    Returns the maximum time the api should wait in seconds when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll.

    This is configurable by the environment variable QCWARE_MAX_WAIT_IN_SECONDS

    The default value is 20 seconds
    """
    result = override if override is not None \
        else config('QCWARE_MAX_WAIT_IN_SECONDS', default=20, cast=int)
    return result


def set_max_wait_in_seconds(new_wait: int):
    os.environ['QCWARE_MAX_WAIT_IN_SECONDS'] = str(new_wait)
