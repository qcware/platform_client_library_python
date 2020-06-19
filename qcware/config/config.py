from decouple import config, UndefinedValueError
from urllib.parse import urlparse, urljoin
from typing import Optional
from packaging import version
import requests
import colorama
from .api_semver import api_semver
import os
import warnings


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


def max_poll_period(override: Optional[int] = None):
    """
    Returns the maximum time the api should retry polling when running
    in synchronous mode before returning the error state that the call
    is not complete and allowing the user to poll manually.

    This is configurable by the environment variable QCWARE_MAX_POLL_PERIOD

    The default value is 60 seconds
    """
    result = override if override is not None \
        else config('QCWARE_MAX_POLL_PERIOD', default=60, cast=int)
    return result


def set_max_poll_period(new_wait: int):
    os.environ['QCWARE_MAX_POLL_PERIOD'] = str(new_wait)


def max_long_poll(override: Optional[int] = None):
    """
    Returns the maximum time the server should sit pinging the database for 
    a result before giving up.

    This is configurable by the environment variable QCWARE_MAX_LONG_POLL

    The default value is 60 seconds
    """
    result = override if override is not None \
        else config('QCWARE_MAX_LONG_POLL', default=60, cast=int)
    return result


def set_max_long_poll(new_wait: int):
    os.environ['QCWARE_MAX_LONG_POLL'] = str(new_wait)
