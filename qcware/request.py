import backoff
import requests

from .exceptions import ApiCallFailedError


def _fatal_code(e):
    return 400 <= e.response.status_code < 500


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=3,
                      giveup=_fatal_code)
def post_request(url, data):
    return requests.post(url, json=data)


def post(url, data):
    response = post_request(url, data)
    if response.status_code >= 400:
        raise ApiCallFailedError(response.json()['message'])
    return response.json()
