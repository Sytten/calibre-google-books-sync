import json

from polyglot.http_client import HTTPSConnection
from polyglot.urllib import urlencode


def post(host, url, payload):
    http = HTTPSConnection(host, timeout=10)
    try:
        params = urlencode(payload)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        http.request("POST", url, params, headers)
        resp = http.getresponse()
    finally:
        http.close()

    return resp


def parse_json(res):
    # FIXME: Something is wrong here, the body is empty
    string = res.read().decode("utf-8")
    return json.loads(string)
