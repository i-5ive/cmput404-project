import requests
import json

from core.authors.models import Author
from core.hostUtil import is_external_host, get_host_url
from core.servers.SafeServerUtil import ServerUtil

from posixpath import join as urljoin

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
    return urljoin(get_host_url(), "author", id)

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
    for authorUrl in authorUrls:
        if (is_external_host(authorUrl)):
            # open a server util with the author url
            sUtil = ServerUtil(authorUrl=authorUrl)
            if not sUtil.valid_server():
                print("authorUrl found, but not in DB", authorUrl)
                continue # We couldn't find a server that matches the friend URL base
            # split the id from the URL and ask the external server about them
            success, authorInfo = sUtil.get_author_info(authorUrl.split("/author/")[1])
            if not success:
                continue # We couldn't successfully fetch from an external server

            # PITA Point: Some servers don't store their IDs as the actual
            # location where you can GET the author summary, just use the ID
            # if you don't want to hate yourself, even though HOST will be
            # the correct location to get the service.
            summaries.append({
                "id": authorUrl,
                "host": sUtil.get_base_url(),
                "url": authorUrl,
                "displayName": authorInfo["displayName"]
            })
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
    return summaries
