import requests
import json

from core.authors.models import Author
from core.hostUtil import is_external_host, get_host_url

def get_author_id(url):
    if (is_external_host(url)):
        return url
    return url.split("author/")[1]

def get_author_url(id):
    return get_host_url() + "/author/" + id

def get_author_summaries(authorUrls):
    summaries = []
    localAuthors = []
    externalHosts = {}
    for authorUrl in authorUrls:
        if (is_external_host(authorUrl)):
            hostUrl = authorUrl.split("author/")[0]
            if (hostUrl in externalHosts):
                externalHosts[hostUrl].append(authorUrl)
            else:
                externalHosts[hostUrl] = [authorUrl]
        else:
            localAuthors.append(get_author_id(authorUrl))
    
    authors = Author.objects.filter(pk__in=localAuthors)
    host = get_host_url()
    for author in authors:
        url = get_author_url(str(author.id))
        summaries.append({
            "id": url,
            "host": host,
            "url": url,
            "displayName": author.get_display_name()
        })

    # requires each external host to set up an endpoint at /authorSummaries
    try:
        for host, authorUrls in externalHosts.items():
            response = requests.post(host + "authorSummaries", data=json.dumps(authorUrls), headers={
                "Content-Type": "application/json"
            })
            summaries += json.loads(response.content)
    except Exception as e:
        print(e)

    return summaries