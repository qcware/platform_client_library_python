from decouple import config, UndefinedValueError
from urllib.parse import urlparse, urljoin
from typing import Optional
from functools import reduce
from packaging import version
import requests
import colorama
from .api_semver import api_semver
import os
from pydantic import BaseModel
from contextlib import contextmanager
import contextvars
from enum import Enum


class ConfigurationError(Exception):
    pass


Client_semver_override = None


def override_client_api_semver(semver: str):
    """
    Sets the API version reported by the client module.  This
    does NOT change any behaviour and is only for testing!
    """
    global Client_semver_override
    Client_semver_override = semver


def client_api_semver() -> str:
    """
    Reports the semantic API version used by the client
    """
    global Client_semver_override
    return Client_semver_override if Client_semver_override is not None else api_semver


def qcware_api_key(override: Optional[str] = None) -> str:
    """
    Returns the API key from environment variable QCWARE_API_KEY, config file,
    or the provided override (if the override is provided, this function simply
    returns the provided override)
    """
    result = override if override is not None else current_context(
    ).credentials.qcware_api_key
    if result is None:
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
        else current_context().qcware_host
    # check to make sure the host is a valid url

    if is_valid_host_url(result):
        return result
    else:
        raise ConfigurationError(
            f"Configured QCWARE_HOST ({result}): does not seem to be"
            "a valid URL.  Please select a host url with scheme"
            "(http or https) and no path, e.g."
            "'http://api.forge.qcware.com'")


def host_api_semver() -> str:
    """
    Returns the semantic API version string reported by the host.
    """
    result = None
    try:
        url = urljoin(qcware_host(), 'about/about')
        r = requests.get(url)
        if r.status_code != 200:
            raise ConfigurationError(
                f'Unable to retrieve API version from host "{qcware_host()}"')
        result = r.json()['api_semver']
    except (AttributeError, requests.exceptions.InvalidSchema) as e:
        raise ConfigurationError(
            f'Error contacting configured host "{qcware_host()}": raised {e}')
    return result


def client_api_incompatibility_message(client_version: version.Version,
                                       host_version: version.Version) -> str:
    """
    Returns an informative string based on the severity of incompatibility between
    client and host API versions
    """
    if client_version.major != host_version.major:
        return colorama.Fore.RED + colorama.Style.BRIGHT \
            + f"\nMajor API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n" \
            + "Likely many calls will fail as the API has changed in incompatible ways.\n" \
            + "Please upgrade with 'pip install --upgrade qcware'" \
            + colorama.Style.RESET_ALL
    elif client_version.major == host_version.major and client_version.minor != host_version.minor:
        return colorama.Fore.YELLOW \
            + f"\nMinor API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n" \
            + "Some calls may act strangely, and you may be missing out on \n"\
            + "new functionality if using an older client.\n" \
            + "Consider upgrading with 'pip install --upgrade qcware'" \
            + colorama.Style.RESET_ALL
    elif client_version.major == host_version.major \
         and client_version.minor == host_version.minor \
         and client_version.micro != host_version.minor:
        return colorama.Fore.GREEN \
            + f"\nMicro API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n" \
            + "You may be missing out on minor bugfixes if using an older client.\n" \
            + "consider upgrading with 'pip install --upgrade qcware'" \
            + colorama.Style.RESET_ALL
    else:
        return ""


Client_api_compatibility_check_has_been_done = False


def do_client_api_compatibility_check(client_version_string: str = None,
                                      host_version_string: str = None):
    """
    Checks the client and host API versions and prints an informative
    string if the versions differ in a material way.
    """
    client_version_string = client_api_semver(
    ) if client_version_string is None else client_version_string
    host_version_string = host_api_semver(
    ) if host_version_string is None else host_version_string
    client_version = version.Version(client_version_string)
    host_version = version.Version(host_version_string)
    if client_version != host_version:
        print(client_api_incompatibility_message(client_version, host_version))
    global Client_api_compatibility_check_has_been_done
    Client_api_compatibility_check_has_been_done = True


def do_client_api_compatibility_check_once(client_version_string: str = None,
                                           host_version_string: str = None):
    """
    If an API compatibility check has not been done between client and the
    selected host, do it now and disable further checks.
    """
    global Client_api_compatibility_check_has_been_done
    if not Client_api_compatibility_check_has_been_done:
        client_version_string = client_api_semver(
        ) if client_version_string is None else client_version_string
        host_version_string = host_api_semver(
        ) if host_version_string is None else host_version_string
        do_client_api_compatibility_check(client_version_string,
                                          host_version_string)


def set_api_key(key: str):
    """
    Set's the user's forge API key via environment variable.
    Equivalent to os.environ['QCWARE_API_KEY']=key
    """
    os.environ['QCWARE_API_KEY'] = key


def set_host(host_url: str):
    if is_valid_host_url(host_url):
        os.environ['QCWARE_HOST'] = host_url
        global Client_api_compatibility_check_has_been_done
        Client_api_compatibility_check_has_been_done = False
    else:
        raise ConfigurationError(
            f"Requested QCWARE_HOST ({host_url}): does not"
            " seem to be a valid URL.  Please select a host url"
            "with scheme (http or https) and no path, e.g."
            "'http://api.forge.qcware.com'")


def client_timeout(override: Optional[int] = None):
    """
    Returns the maximum time the api should retry polling when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll manually.

    This is configurable by the environment variable QCWARE_CLIENT_TIMEOUT

    The default value is 60 seconds
    """
    result = override if override is not None \
        else current_context().client_timeout
    return result


def set_client_timeout(new_wait: int):
    """
    Sets the maximum time the API should retry polling the server before
    returning the error state that the call is not complete.

    This may be set to any value greater than or equal to 0 seconds.
    """
    if new_wait < 0:
        print(colorama.Fore.YELLOW +
              "Client timeout must be >= 0 seconds; no action taken" +
              colorama.Style.RESET_ALL)
    else:
        os.environ['QCWARE_CLIENT_TIMEOUT'] = str(new_wait)


def server_timeout(override: Optional[int] = None):
    """
    Returns the maximum time the api should retry polling when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll manually.

    This is configurable by the environment variable QCWARE_CLIENT_TIMEOUT

    The default value is 60 seconds
    """
    result = override if override is not None \
        else current_context().server_timeout
    return result


def set_server_timeout(new_wait: int):
    """
    Sets the maximum time the API should retry polling the server before
    returning the error state that the call is not complete.

    This may be set to any value greater than or equal to 0 seconds.
    """
    if new_wait < 0 or new_wait > 50:
        print(
            colorama.Fore.YELLOW +
            "Server timeout must be between 0 and 50 seconds; no action taken"
            + colorama.Style.RESET_ALL)
    else:
        os.environ['QCWARE_SERVER_TIMEOUT'] = str(new_wait)


def async_interval_between_tries(override: Optional[float] = None):
    """
    Returns the maximum time the server should sit pinging the database for 
    a result before giving up.

    This is configurable by the environment variable QCWARE_SERVER_TIMEOUT

    The default value is 10 seconds; the maximum is 50
    """
    result = override if override is not None \
        else current_context().async_interval_between_tries
    return result


def set_async_interval_between_tries(new_interval: float):
    """
    Sets the maximum server timeout (how long the server will poll for a result
    before returning to the client with a result or 'still waiting' message.  

    Normally the user should not change this from the default value of 10s.
    """
    if new_interval < 0 or new_interval > 50:
        print(
            colorama.Fore.YELLOW +
            "Time between async tries must be between 0 and 50 seconds; no action taken"
            + colorama.Style.RESET_ALL)
    else:
        os.environ['QCWARE_ASYNC_INTERVAL_BETWEEN_TRIES'] = str(new_interval)


class SchedulingMode(str, Enum):
    immediate = 'immediate'
    next_available = 'next_available'


def scheduling_mode(override: Optional[SchedulingMode] = None):
    """
    Returns the scheduling mode, only relevant for backends that have availability
    windows.  "immediate" means a call should fail if called for outside its
    availability window, while "next_available" means such calls should be automaticall
    scheduled for the next availability window.

    A reschedule is not a guarantee that the job will be run within that window!  If not,
    it will stay in the queue until the next availability window.
    """
    result = override if override is not None \
        else current_context().scheduling_mode
    return result


def set_scheduling_mode(new_mode: SchedulingMode):
    """
    Sets the scheduling mode, only relevant for backends that have availability
    windows.  "immediate" means a call should fail if called for outside its
    availability window, while "next_available" means such calls should be automaticall
    scheduled for the next availability window.

    A reschedule is not a guarantee that the job will be run within that window!  If not,
    it will stay in the queue until the next availability window.
    """
    new_value = SchedulingMode(new_mode)
    os.environ['QCWARE_SCHEDULING_MODE'] = new_value.value


class ApiCredentials(BaseModel):
    qcware_api_key: Optional[str] = None


class ApiCallContext(BaseModel):
    qcware_host: Optional[str] = None
    credentials: Optional[ApiCredentials] = None
    server_timeout: Optional[int] = None
    client_timeout: Optional[int] = None
    async_interval_between_tries: Optional[float] = None
    scheduling_mode: Optional[SchedulingMode] = None

    class Config:
        extra = 'forbid'


def root_context() -> ApiCallContext:
    """
    Returns a dictionary containing relevant information for API calls; used internally
    """
    return ApiCallContext(
        qcware_host=config('QCWARE_HOST', 'https://api.forge.qcware.com'),
        credentials=ApiCredentials(
            qcware_api_key=config('QCWARE_API_KEY', None)),
        server_timeout=config('QCWARE_SERVER_TIMEOUT', default=10, cast=int),
        client_timeout=config('QCWARE_CLIENT_TIMEOUT', default=60, cast=int),
        async_interval_between_tries=config(
            'QCWARE_ASYNC_INTERVAL_BETWEEN_TRIES', 0.5, cast=float),
        scheduling_mode=config('QCWARE_SCHEDULING_MODE',
                               default=SchedulingMode.immediate))


_contexts = contextvars.ContextVar('contexts', default=[])


def push_context(**kwargs):
    """
    Manually pushes a configuration context onto the stack; normally 
    this is done with the `additional_config` context rather than called
    directly by the user
    """
    next_context = ApiCallContext(**kwargs)
    _contexts.set(_contexts.get() + [next_context])


def pop_context():
    """
    Manually pops a configuration context from the stack; normally
    this is done with the `additional_config` context rather than called
    directly by the user
    """
    _contexts.set(_contexts.get()[:-1])


def current_context() -> ApiCallContext:
    """
    Returns the "current context" for an API call, which is the calculated
    root context plus any additional changes through the stack.  Normally
    not called by the user.
    """
    def merge_contexts(c1, c2):
        return c1.copy(
            update={k: v
                    for k, v in c2.dict().items() if v is not None})

    return reduce(merge_contexts, _contexts.get(), root_context())


@contextmanager
def additional_config(**kwargs):
    """
    This provides a context manager through which the qcware python client library
    can be temporarily reconfigured, for example to allow a longer client timeout for a
    call, or to make a call with different credentials.  To use it, one must provide
    a set of keywords which map to the arguments of an `ApiCallContext`, for example, to
    make a single call with a client timout of five minutes:

    ```
    with additional_config(client_tiemout=5*60):
        result = solve_binary(...)
    ```
    """
    push_context(**kwargs)
    try:
        yield
    finally:
        pop_context()
