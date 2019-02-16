host = request.get_host()

def is_external_host(url):
	return host not in url
