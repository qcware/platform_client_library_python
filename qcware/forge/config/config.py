import contextvars
import os
import sys
from contextlib import contextmanager
from enum import Enum
from functools import reduce
from typing import Optional
from urllib.parse import urljoin, urlparse

import colorama  # type: ignore
import requests
from decouple import config  # type: ignore
from packaging import version
from pydantic import BaseModel, ConstrainedStr, Field
from qcware.forge import __version__ as Qcware_client_version
from qcware.forge.config.api_semver import api_semver


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
    result = (
        override
        if override is not None
        else current_context().credentials.qcware_api_key  # type:ignore
    )
    if result is None:
        raise ConfigurationError(
            "You have not provided a QCWare API key.  "
            "Please set one with the argument api_key, "
            "by calling qcware.set_api_key, or via "
            "configuration variables or files."
        )
    return result


def is_valid_host_url(url: Optional[str]) -> bool:
    """
    Checks if a host url is valid.  A valid host url is just a scheme
    (http/https), a net location, and no path.
    """
    if url is None:
        result = False
    else:
        parse_result = urlparse(url)
        result = (
            all([parse_result.scheme, parse_result.netloc]) and not parse_result.path
        )
    return result


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
    result = override if override is not None else current_context().qcware_host
    # check to make sure the host is a valid url

    if is_valid_host_url(result):
        # type ignored below because if we get here, it's a valid string
        return result  # type:ignore
    else:
        raise ConfigurationError(
            f"Configured QCWARE_HOST ({result}): does not seem to be"
            "a valid URL.  Please select a host url with scheme"
            "(http or https) and no path, e.g."
            "'http://api.forge.qcware.com'"
        )


def host_api_semver() -> str:
    """
    Returns the semantic API version string reported by the host.
    """
    result = None
    try:
        url = urljoin(qcware_host(), "about/about")
        r = requests.get(url)
        if r.status_code != 200:
            raise ConfigurationError(
                f'Unable to retrieve API version from host "{qcware_host()}"'
            )
        result = r.json()["api_semver"]
    except (AttributeError, requests.exceptions.InvalidSchema) as e:
        raise ConfigurationError(
            f'Error contacting configured host "{qcware_host()}": raised {e}'
        )
    return result


def client_api_incompatibility_message(
    client_version: version.Version, host_version: version.Version
) -> str:
    """
    Returns an informative string based on the severity of incompatibility between
    client and host API versions
    """
    if client_version.major != host_version.major:
        return (
            colorama.Fore.RED
            + colorama.Style.BRIGHT
            + f"\nMajor API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n"
            + "Likely many calls will fail as the API has changed in incompatible ways.\n"
            + "Please upgrade with 'pip install --upgrade qcware'"
            + colorama.Style.RESET_ALL
        )
    elif (
        client_version.major == host_version.major
        and client_version.minor != host_version.minor
    ):
        return (
            colorama.Fore.YELLOW
            + f"\nMinor API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n"
            + "Some calls may act strangely, and you may be missing out on \n"
            + "new functionality if using an older client.\n"
            + "Consider upgrading with 'pip install --upgrade qcware'"
            + colorama.Style.RESET_ALL
        )
    elif (
        client_version.major == host_version.major
        and client_version.minor == host_version.minor
        and client_version.micro != host_version.minor
    ):
        return (
            colorama.Fore.GREEN
            + f"\nMicro API version incompatibility (you: {str(client_version)}; host: {str(host_version)})\n"
            + "You may be missing out on minor bugfixes if using an older client.\n"
            + "consider upgrading with 'pip install --upgrade qcware'"
            + colorama.Style.RESET_ALL
        )
    else:
        return ""


Client_api_compatibility_check_has_been_done = False


def do_client_api_compatibility_check(
    client_version_string: str = None, host_version_string: str = None
):
    """
    Checks the client and host API versions and prints an informative
    string if the versions differ in a material way.
    """
    client_version_string = (
        client_api_semver() if client_version_string is None else client_version_string
    )
    host_version_string = (
        host_api_semver() if host_version_string is None else host_version_string
    )
    client_version = version.Version(client_version_string)
    host_version = version.Version(host_version_string)
    if client_version != host_version:
        print(client_api_incompatibility_message(client_version, host_version))
    global Client_api_compatibility_check_has_been_done
    Client_api_compatibility_check_has_been_done = True


def do_client_api_compatibility_check_once(
    client_version_string: str = None, host_version_string: str = None
):
    """
    If an API compatibility check has not been done between client and the
    selected host, do it now and disable further checks.
    """
    global Client_api_compatibility_check_has_been_done
    if not Client_api_compatibility_check_has_been_done:
        client_version_string = (
            client_api_semver()
            if client_version_string is None
            else client_version_string
        )
        host_version_string = (
            host_api_semver() if host_version_string is None else host_version_string
        )
        do_client_api_compatibility_check(client_version_string, host_version_string)


def set_api_key(key: str):
    """
    Set's the user's forge API key via environment variable.
    Equivalent to os.environ['QCWARE_API_KEY']=key
    """
    os.environ["QCWARE_API_KEY"] = key


def set_host(host_url: str):
    if is_valid_host_url(host_url):
        os.environ["QCWARE_HOST"] = host_url
        global Client_api_compatibility_check_has_been_done
        Client_api_compatibility_check_has_been_done = False
    else:
        raise ConfigurationError(
            f"Requested QCWARE_HOST ({host_url}): does not"
            " seem to be a valid URL.  Please select a host url"
            "with scheme (http or https) and no path, e.g."
            "'http://api.forge.qcware.com'"
        )


def client_timeout(override: Optional[int] = None):
    """
    Returns the maximum time the api should retry polling when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll manually.

    This is configurable by the environment variable QCWARE_CLIENT_TIMEOUT

    The default value is 60 seconds
    """
    result = override if override is not None else current_context().client_timeout
    return result


def set_client_timeout(new_wait: int):
    """
    Sets the maximum time the API should retry polling the server before
    returning the error state that the call is not complete.

    This may be set to any value greater than or equal to 0 seconds.
    """
    if new_wait < 0:
        print(
            colorama.Fore.YELLOW
            + "Client timeout must be >= 0 seconds; no action taken"
            + colorama.Style.RESET_ALL
        )
    else:
        os.environ["QCWARE_CLIENT_TIMEOUT"] = str(new_wait)


def server_timeout(override: Optional[int] = None):
    """
    Returns the maximum time the api should retry polling when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll manually.

    This is configurable by the environment variable QCWARE_CLIENT_TIMEOUT

    The default value is 60 seconds
    """
    result = override if override is not None else current_context().server_timeout
    return result


def set_server_timeout(new_wait: int):
    """
    Sets the maximum time the API should retry polling the server before
    returning the error state that the call is not complete.

    This may be set to any value greater than or equal to 0 seconds.
    """
    if new_wait < 0 or new_wait > 50:
        print(
            colorama.Fore.YELLOW
            + "Server timeout must be between 0 and 50 seconds; no action taken"
            + colorama.Style.RESET_ALL
        )
    else:
        os.environ["QCWARE_SERVER_TIMEOUT"] = str(new_wait)


def async_interval_between_tries(override: Optional[float] = None):
    """Return the maximum time the server should sit pinging the database
    for a result before giving up.

    This is configurable by the environment variable QCWARE_SERVER_TIMEOUT

    The default value is 10 seconds; the maximum is 50

    """
    result = (
        override
        if override is not None
        else current_context().async_interval_between_tries
    )
    return result


def set_async_interval_between_tries(new_interval: float):
    """Set the maximum server timeout.

    This sets how long the server will poll for a result before
    returning to the client with a result or 'still waiting' message.

    Normally the user should not change this from the default value of 10s.

    """
    if new_interval < 0 or new_interval > 50:
        print(
            colorama.Fore.YELLOW
            + "Time between async tries must be between 0 and 50 seconds; no action taken"
            + colorama.Style.RESET_ALL
        )
    else:
        os.environ["QCWARE_ASYNC_INTERVAL_BETWEEN_TRIES"] = str(new_interval)


class SchedulingMode(str, Enum):
    """Scheduling modes for API calls.

    'immediate' means 'attempt this now; if it must be rescheduled
    (such as for an unavailable backend), fail with an exception'

    'next_available' means 'attempt this now, but if the backend is
    unavailable, schedule during the next availability window.'

    """

    immediate = "immediate"
    next_available = "next_available"


def scheduling_mode(override: Optional[SchedulingMode] = None):
    """
    Returns the scheduling mode, only relevant for backends that have availability
    windows.  "immediate" means a call should fail if called for outside its
    availability window, while "next_available" means such calls should be automaticall
    scheduled for the next availability window.

    A reschedule is not a guarantee that the job will be run within that window!  If not,
    it will stay in the queue until the next availability window.
    """
    result = override if override is not None else current_context().scheduling_mode
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
    os.environ["QCWARE_SCHEDULING_MODE"] = new_value.value


def set_ibmq_credentials(
    token: Optional[str] = None,
    hub: Optional[str] = None,
    group: Optional[str] = None,
    project: Optional[str] = None,
):
    """Set the IBMQ credentials "by hand"."""

    def _set_if(envvar_name: str, value: Optional[str] = None):
        if value is None and envvar_name in os.environ:
            del os.environ[envvar_name]
        elif value is not None:
            os.environ[envvar_name] = value

    _set_if("QCWARE_CRED_IBMQ_TOKEN", token)
    _set_if("QCWARE_CRED_IBMQ_HUB", hub)
    _set_if("QCWARE_CRED_IBMQ_GROUP", group)
    _set_if("QCWARE_CRED_IBMQ_PROJECT", project)


def set_ibmq_credentials_from_ibmq_provider(
    provider: "qiskit.providers.ibmq.accountprovider.AccountProvider",
):
    """Set the IBMQ credentials from an ibmq provider object.

    Called normally as set_ibmq_credentials_from_ibmq(IBMQ.providers()[0]).
    The IBMQ "factory" can provide several providers, particularly if your
    IBMQ token is associated with various hubs, groups, or projects.

    """
    set_ibmq_credentials(
        provider.credentials.token,
        provider.credentials.hub,
        provider.credentials.group,
        provider.credentials.project,
    )


class IBMQCredentials(BaseModel):

    token: Optional[str]
    hub: Optional[str]
    group: Optional[str]
    project: Optional[str]

    @classmethod
    def from_ibmq(cls, ibmq):
        """Creates the IBMQ credentials from an existing initialized
        IBMQFactory object.  To be used as

            from qiskit import IBMQ
            IBMQ.load_account() # or enable_account(...)
            credentials=IBMQCredentials.from_ibmq(IBMQ)
        """
        return cls(
            token=ibmq._credentials.token,
            hub=ibmq._credentials.hub,
            group=ibmq._credentials.group,
            project=ibmq._credentials.project,
        )

    class Config:
        extra = "forbid"


class ApiCredentials(BaseModel):
    qcware_api_key: Optional[str] = None
    ibmq: Optional[IBMQCredentials] = None

    class Config:
        extra = "forbid"


class Environment(BaseModel):
    """This deserves a little explanation; it is greatly helpful to us
    when diagnosing a problem to have recorded information about the
    "environment" of the call.  These are manually overloadable should
    users wish to hide this information, but it is set by default in this
    fashion:

    client, client_version: usually "qcware" and this library's version

    version environment: the sort of "global environment".  Usually
    this is set by environment variable
    "QCWARE_ENVIRONMENT_ENVIRONMENT", which is "hosted_jupyter"on
    hosted jupyter notebooks, or "local" for a local installation.

    source_file: this is empty by default so that we do not collect
    unnecessary information from users.  It is set in our hosted example
    notebooks so that we can see what calls come from example notebooks.
    This is set via the environment variable QCWARE_ENVIRONMENT_SOURCE_FILE.
    """

    client: str
    client_version: str
    python_version: str
    environment: str
    source_file: str


def set_environment_environment(new_environment: str):
    """Set the Environment ... environment."""
    os.environ["QCWARE_ENVIRONMENT_ENVIRONMENT"] = new_environment


def set_environment_source_file(new_source_file: str):
    """Set the source file recorded in the context environment."""
    os.environ["QCWARE_ENVIRONMENT_SOURCE_FILE"] = new_source_file


class ApiCallContext(BaseModel):
    """The context sent over with every API call.

    A number of things are listed as "optional" which really are not; they are
    created by default in the `root_context` function.  By allowing them to be
    optional, you can augment the current context with "temporary contexts" that
    override only one field (or a subset).
    """

    qcware_host: Optional[str] = None
    credentials: Optional[ApiCredentials] = None
    environment: Optional[Environment] = None
    server_timeout: Optional[int] = None
    client_timeout: Optional[int] = None
    async_interval_between_tries: Optional[float] = None
    scheduling_mode: Optional[SchedulingMode] = None

    class Config:
        extra = "forbid"


def root_context() -> ApiCallContext:
    """
    Return a dictionary containing relevant information for API calls.

    Used internally
    """
    return ApiCallContext(
        qcware_host=config("QCWARE_HOST", "https://api.forge.qcware.com"),
        credentials=ApiCredentials(
            qcware_api_key=config("QCWARE_API_KEY", None),
            ibmq=IBMQCredentials(
                token=config("QCWARE_CRED_IBMQ_TOKEN", None),
                hub=config("QCWARE_CRED_IBMQ_HUB", None),
                group=config("QCWARE_CRED_IBMQ_GROUP", None),
                project=config("QCWARE_CRED_IBMQ_PROJECT", None),
            ),
        ),
        environment=Environment(
            client="qcware (python)",
            client_version=Qcware_client_version,
            python_version=sys.version,
            environment=config("QCWARE_ENVIRONMENT_ENVIRONMENT", default="local"),
            source_file=config("QCWARE_ENVIRONMENT_SOURCE_FILE", default=""),
        ),
        server_timeout=config("QCWARE_SERVER_TIMEOUT", default=10, cast=int),
        client_timeout=config("QCWARE_CLIENT_TIMEOUT", default=60, cast=int),
        async_interval_between_tries=config(
            "QCWARE_ASYNC_INTERVAL_BETWEEN_TRIES", 0.5, cast=float
        ),
        scheduling_mode=config(
            "QCWARE_SCHEDULING_MODE", default=SchedulingMode.immediate
        ),
    )


_contexts: contextvars.ContextVar[ApiCallContext] = contextvars.ContextVar(
    "contexts", default=[]
)  # type:ignore


def push_context(**kwargs):
    """Manually pushes a configuration context onto the stack.

    Normally this is done with the `additional_config` context rather
    than called directly by the user

    """
    next_context = ApiCallContext(**kwargs)
    _contexts.set(_contexts.get() + [next_context])


def pop_context():
    """Manually pops a configuration context from the stack.

    Normally this is done with the `additional_config` context rather
    than called directly by the user

    """
    _contexts.set(_contexts.get()[:-1])


# from https://github.com/pytoolz/toolz/issues/281
# although as noted more efficient solutions exist.  This is also
# modified to ignore k/v pairs in b for which the value is None
def deep_merge(a, b):
    """Merge two dictionaries recursively."""

    def merge_values(k, v1, v2):
        if isinstance(v1, dict) and isinstance(v2, dict):
            return k, deep_merge(v1, v2)
        elif v2 is not None:
            return k, v2
        else:
            return k, v1

    a_keys = set(a.keys())
    b_keys = set(b.keys())
    pairs = (
        [merge_values(k, a[k], b[k]) for k in a_keys & b_keys]
        + [(k, a[k]) for k in a_keys - b_keys]
        + [(k, b[k]) for k in b_keys - a_keys]
    )
    return dict(pairs)


def merge_models(c1: BaseModel, c2: BaseModel) -> BaseModel:
    d1 = c1.dict()
    d2 = c2.dict()
    result_dict = deep_merge(d1, d2)
    return c1.copy(update=result_dict)


def current_context() -> ApiCallContext:
    """Return the "current context" for an API call.

    This is the calculated root context plus any additional changes
    through the stack.  Normally not called by the user.

    """
    # known problem below with mypy and reduce, see https://github.com/python/mypy/issues/4150
    # among others
    return reduce(merge_models, _contexts.get(), root_context())  # type:ignore


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
        result = optimize_binary(...)
    ```
    """
    push_context(**kwargs)
    try:
        yield
    finally:
        pop_context()


@contextmanager
def ibmq_credentials(
    token: str,
    hub: Optional[str] = None,
    group: Optional[str] = None,
    project: Optional[str] = None,
):
    ibmq_creds = IBMQCredentials(token=token, hub=hub, group=group, project=project)
    credentials = ApiCredentials(ibmq=ibmq_creds)
    push_context(credentials=credentials)
    try:
        yield
    finally:
        pop_context()


@contextmanager
def ibmq_credentials_from_ibmq(ibmq):
    ibmq_creds = IBMQCredentials.from_ibmq(ibmq)
    credentials = ApiCredentials(ibmq=ibmq_creds)
    push_context(credentials=credentials)
    try:
        yield
    finally:
        pop_context()
