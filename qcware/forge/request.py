import backoff
import requests

from qcware.forge.exceptions import ApiCallFailedError, ApiCallResultUnavailableError

_client_session = None


def client_session() -> requests.Session:
    """
    Singleton guardian for client session
    """
    global _client_session
    if _client_session is None:
        _client_session = requests.Session()
    return _client_session


def _fatal_code(e):
    return 400 <= e.response.status_code < 500


@backoff.on_exception(
    backoff.expo, requests.exceptions.RequestException, max_tries=3, giveup=_fatal_code
)
def post_request(url, data):
    return client_session().post(url, json=data)


@backoff.on_exception(
    backoff.expo, requests.exceptions.RequestException, max_tries=3, giveup=_fatal_code
)
def get_request(url):
    return client_session().get(url)


def post(url, data):
    response = post_request(url, data)
    if response.status_code >= 400:
        print(response)
        raise ApiCallFailedError(response.json()["message"])
    return response.json()


def get(url):
    response = get_request(url)
    if response.status_code >= 400:
        raise ApiCallResultUnavailableError(
            "Unable to retrieve result, please try again later or contact support"
        )
    return response.text
