import os
host = os.environ.get("DJANGO_SITE_URL") or "http://127.0.0.1:8000"

def is_external_host(url):
    return host not in url

def get_host_url():
    return host