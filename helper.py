import os

proxy_http = os.environ.get('PROXY_HTTP')
proxy_https = os.environ.get('PROXY_HTTPS')


def get_proxies():
    proxies = {}

    if proxy_http:
        proxies['http'] = proxy_http

    if proxy_https:
        proxies['https'] = proxy_https

    return proxies
