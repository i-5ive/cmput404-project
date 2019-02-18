from core.hostUtil import is_external_host, get_host_url

def get_author_id(url):
    if (is_external_host(url)):
        return url
    return url.split("author/")[1]

def get_author_url(id):
    return get_host_url() + "/author/" + id