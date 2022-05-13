import requests
from fake_headers import Headers


def get_html(url, params=None):
    headers = Headers(headers=True)
    r = requests.get(url, headers=headers.generate(), params=params)
    r.encoding = 'utf8'
    return r
