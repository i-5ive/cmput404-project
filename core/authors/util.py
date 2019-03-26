import requests
import json

from core.authors.models import Author
from core.hostUtil import is_external_host, get_host_url

from core.servers.SafeServerUtil import ServerUtil

## Gets the unique ID of a local or external author. If external, returns the URL. If local, returns just the uuid
## @param {String} url - the unique URL of the author
## @return {String} - the unique ID used to refer to the author
def get_author_id(url):
    if (is_external_host(url)):
        return url
    return url.split("author/")[1]

## Gets the unique URL of the specified local author
## @param {String} id - the author's unique ID
## @return {String} - the unique URL to the author
def get_author_url(id):
    return get_host_url() + "/author/" + id

## Gets a summary of each specified author
## @param {List<String>} authorUrls - a list of author URLs to get details from (can be both external and internal)
## @return {List<Object>} - a summary of each author, in the form:
## {
##      url: String
##      displayName: String
##      id: String
##      host: String
## }
def get_author_summaries(authorUrls):
    summaries = []
    localAuthors = []
    externalHosts = {}
    for authorUrl in authorUrls:
        if (is_external_host(authorUrl)):
            # remove the beginning slash because we don't store ending slashes in Servers.
            hostUrl = authorUrl.split("/author/")[0]
            print("searching host url", hostUrl)
            hostUrl = ServerUtil.get_base_url_from_similar_name(hostUrl)
            print("updated hostUrl", hostUrl)
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

    # try each user (we shouldn't stop checking externals just because one failed)
    # requires each external host to set up an endpoint at /authorSummaries
    for host, authorUrls in externalHosts.items():
        try:
            # Host is not ended with a slash so we add it here
            print("trying:", host + "/authorSummaries")
            response = requests.post(host + "/authorSummaries", data=json.dumps(authorUrls), headers={
                "Content-Type": "application/json"
            })
            print("success:", json.loads(response.content))
            summaries += json.loads(response.content)
        except Exception as e:
            print("failed" , e)

    return summaries