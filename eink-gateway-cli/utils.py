import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode


def native_request(method: str, url: str, query: dict = None, data: bytes = None, headers: dict = None) -> bytes | HTTPError:
    url_with_query = url if not query else url + '?' + urlencode(query)
    request_config = Request(url_with_query, data=data, headers=headers, method=method)

    try:
        with urlopen(request_config) as response:
            return response.read()
    except HTTPError as e:
        return e


def http_get(url: str, query: dict = None, headers: dict = None) -> bytes | HTTPError:
    return native_request('GET', url, query, None, headers)


def http_post(url: str, query: dict = None, data: bytes = None, headers: dict = None) -> bytes | HTTPError:
    return native_request('POST', url, query, data, headers)


def json_get(url: str, query: dict = None, headers: dict = None) -> dict | HTTPError:
    headers = headers or {}
    json_header = {'Content-Type': 'application/json'}

    response = http_get(url=url, query=query, headers={**json_header, **headers})

    if isinstance(response, HTTPError):
        return response

    if not response:
        return {}

    return json.loads(response)


def json_post(url: str, query: dict = None, data: dict = None, headers: dict = None) -> dict | HTTPError:
    headers = headers or {}
    json_header = {'Content-Type': 'application/json'}

    response = http_post(url=url, query=query, data=json.dumps(data).encode('utf-8'), headers={**json_header, **headers})

    if isinstance(response, HTTPError):
        return response

    if not response:
        return {}

    return json.loads(response)
