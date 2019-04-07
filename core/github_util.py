import requests
import json
import re

from posixpath import join as urljoin

from core.hostUtil import get_host_url
from core.posts.serializers import PostsSerializer

github_headers = {"Content-Type": "application/json"}

# Credit to Jossef Harush for this: https://stackoverflow.com/a/37697078
def get_event_title(event_type):
    return " ".join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', event_type).split())

def fetch_github_events(github_url):
    res = requests.get(github_url, headers=github_headers)
    if (res.status_code == 200):
        return res.json()
    return []

# https://developer.github.com/v3/activity/events/types/
# Credit goes to azu for this JavaScript/TypeScript code: https://github.com/azu/parse-github-event/blob/master/src/parse-github-event.ts#L84
# MIT License: the event handling is mostly a transformation of his code into Python form
# azu's github profile: https://github.com/azu
def get_event_data(type, payload, repo_name):
    if (type == "CreateEvent"):
        ref_type = payload["ref_type"]
        if (ref_type == "repository"):
            return ("Created the {0} repository".format(repo_name), repo_name)
        elif (ref_type == "tag"):
            return ("Created the {0} tag at {1}".format(payload["ref"], repo_name), urljoin(repo_name, "releases/tag", payload["ref"]))
        elif (ref_type == "branch"):
            return ("Created the {0} branch at {1}".format(payload["ref"], repo_name), urljoin(repo_name, "tree", payload["ref"]))
    elif (type == "MemberEvent"):
        action = payload["action"]
        username = payload["member"]["login"]
        if (action == "added"):
            return ("Added {0} to {1}".format(username, repo_name), username)
        elif (action == "edited"):
            return ("Edited {0}'s permissions at {1}".format(username, repo_name), username)
    elif (type == "PushEvent"):
        branch = payload["ref"].rsplit("/", 1)[1]
        return ("Pushed to {0} at {1}".format(branch, repo_name), urljoin(repo_name, "compare", payload["before"] + "..." + payload["head"]))
    elif (type == "ForkApplyEvent"):
        return ("Merged to {0}".format(repo_name), repo_name)
    elif (type == "ForkEvent"):
        return ("Forked {0}".format(repo_name), payload["forkee"]["html_url"])
    elif (type == "WatchEvent"):
        if (payload["action"] == "started"):
            return ("Starred {0}".format(repo_name), repo_name)
    elif (type == "FollowEvent"):
        return ("Followed {0}".format(payload["target"]["login"]), payload["target"]["login"])
    elif (type == "IssuesEvent" or type == "PullRequestEvent"):
        name = "pull request" if type == "PullRequestEvent" else "issue"
        details = payload["pull_request"] if type == "PullRequestEvent" else payload["issue"]
        action = payload["action"].capitalize()
        return ("{0} {1} {2} at {3}".format(action, name, details["number"], repo_name), details["html_url"])
    elif (type == "GistEvent"):
        action = payload["action"].capitalize() + "ed"
        return ("{0} gist {1}".format(action, payload["gist"]["id"]), payload["gist"]["html_url"])
    elif (type == "CommitCommentEvent"):
        return ("Commented at {0}".format(repo_name), payload["comment"]["html_url"])
    elif (type == "PullRequestReviewCommentEvent"):
        return ("Reviewd pull request {0} at {0}".format(payload["pull_request"]["number"], repo_name), payload["comment"]["html_url"])
    elif (type == "IssueCommentEvent"):
        return ("Commented on issue {0} at {1}".format(payload["issue"]["number"], repo_name), payload["comment"]["html_url"])
    elif (type == "DeleteEvent"):
        return ("Deleted {0} {1} at {2}".format(payload["ref_type"], payload["ref"], repo_name), repo_name)
    elif (type == "PublicEvent"):
        return ("Made {0} public".format(repo_name), repo_name)
        
    return type, repo_name

def parse_event(author, event):
    user_details = event.get("actor") or event.get("sender")
    repo_name = event["repo"]["name"] if event.get("repo") else ""
    content, path = get_event_data(event["type"], event["payload"], repo_name)
    if ("https://" not in path):
        event_url = urljoin("https://github.com", path)
    else:
        event_url = path
    
    post_data = {
        "contentType": "text/markdown",
        "origin": event_url,
        "content": "[{0}]({1})".format(content, event_url),
        "author": author,
        "title": get_event_title(event["type"]),
        "description": "{0} at {1}".format(event["type"], repo_name),
        "categories": ["github", event["type"]],
        "visibility": "PUBLIC",
        "unlisted": False,
        "visibleTo": []
    }
    serializer = PostsSerializer(data=post_data)
    serializer.is_valid()
    post = serializer.create_temporary(serializer.validated_data)
    post.published = event["created_at"].replace("Z", ".000Z")
    return post

def parse_github_events(author, events):
    parsed_results = []
    for event in events:
        parsed = parse_event(author.id, event)
        parsed_results.append(parsed)
    return parsed_results

def get_github_activity(author):
    github_url = author.github
    if (not github_url):
        return []
    if (github_url.endswith("/")):
        github_url = github_url[:-1]

    api_url = "https://api.github.com/users/{0}/events".format(github_url.rsplit("/", 1)[1])
    events = fetch_github_events(api_url)
    posts = parse_github_events(author, events)
    return posts
