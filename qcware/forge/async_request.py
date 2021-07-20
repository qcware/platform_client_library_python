import backoff
import requests
import asyncio
import aiohttp

from qcware.forge.exceptions import ApiCallFailedError, ApiCallResultUnavailableError

_client_session = None


def client_session() -> aiohttp.ClientSession:
    """
    Singleton guardian for client session.  This may need to be moved
    to being a contextvar, and it could be that the whole python Client
    needs to be made instantiable (for sessions).  But since aiohttp is
    single-threaded this should be OK for now.
    """
    global _client_session
    if _client_session is None:
        _client_session = aiohttp.ClientSession()
    return _client_session


def _fatal_code(e):
    return 400 <= e.response.status_code < 500


# By default, evidently aiohttp doesn't raise exceptions for non-200
# statuses, so backoff has trouble unless you specifically ask
# using raise_for_status = True; see
# https://stackoverflow.com/questions/56152651/how-to-retry-async-aiohttp-requests-depending-on-the-status-code


@backoff.on_exception(
    backoff.expo, requests.exceptions.RequestException, max_tries=3, giveup=_fatal_code
)
def post_request(url, data):
    return client_session().post(url, json=data, raise_for_status=True)


@backoff.on_exception(
    backoff.expo, requests.exceptions.RequestException, max_tries=3, giveup=_fatal_code
)
def get_request(url):
    return client_session().get(url, raise_for_status=True)


async def post(url, data):
    async with post_request(url, data) as response:
        if response.status >= 400:
            raise ApiCallFailedError(response.json()["message"])
        return await response.json()


async def get(url):
    async with get_request(url) as response:
        if response.status >= 400:
            raise ApiCallResultUnavailableError(
                "Unable to retrieve result, please try again later or contact support"
            )
        return await response.text()
