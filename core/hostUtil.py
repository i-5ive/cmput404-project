import os
host = os.environ.get("DJANGO_SITE_URL") or "https://unfortunate.herokuapp.com"

def is_external_host(url):
    return host not in url

def get_host_url():
    return host

def is_encoded_external_host(value):
    # base64 encoding of https://
    return value.startswith("aHR0cHM6Ly")