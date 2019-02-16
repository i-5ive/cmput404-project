from core.hostUtil import is_external_host

def get_author_id(url):
	if (is_external_host(url)):
		return url
	return url.split("author/")[1]