import socket
# TODO: fix this
host = socket.gethostname()

def is_external_host(url):
    return host not in url
