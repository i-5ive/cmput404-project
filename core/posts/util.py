from core.authors.friends_util import get_friends_set, get_friends
from core.posts.models import Posts
from core.hostUtil import get_host_url

from posixpath import join as urljoin

## Gets whether the specified user can view a specific post
## @param {User} user - the user to check
## @param {Posts} post - the post to check
## @return {boolean} - whether the user can view the post or not
def can_user_view(user, post):
    if (user.is_authenticated and user.author == post.author):
        return True
    elif ((not user.is_authenticated) and post.visibility != "PUBLIC"):
        return False
    elif (post.visibility == "PUBLIC"):
        return True
    elif (post.visibility == "PRIVATE"):
        return user.author.get_url() in post.visibleTo
    elif (post.visibility == "FRIENDS" or post.visibility == "SERVERONLY"):
        friends = get_friends(post.author.get_url())
        return user.author.get_url() in friends
    elif (post.visibility == "FOAF"):
        author_url = post.author.get_url()
        requester_friends = get_friends_set(user.author.get_url())
        author_friends = get_friends_set(author_url)
        mutual_friends = requester_friends & author_friends
        return len(mutual_friends) > 0
    return False

## Gets whether the specified external user can view a specific post
## @param {String} author_url - the url of the author to check
## @param {Posts} post - the post to check
## @return {boolean} - whether the user can view the post or not
def can_external_user_view(author_url, post):
    if (author_url == None or post.visibility == "SERVERONLY"):
        return False
    elif (post.visibility == "PUBLIC"):
        return True
    elif (post.visibility == "PRIVATE"):
        return author_url in post.visibleTo
    elif (post.visibility == "FRIENDS"):
        friends = get_friends(post.author.get_url())
        return author_url in friends
    elif (post.visibility == "FOAF"):
        post_author_url = post.author.get_url()
        requester_friends = get_friends_set(author_url)
        author_friends = get_friends_set(post_author_url)
        mutual_friends = requester_friends & author_friends
        return len(mutual_friends) > 0

def add_page_details_to_response(request, response_data, page, queryPage):
    # build_absolute_uri is from https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.build_absolute_uri
    if (page.has_previous()):
        response_data["previous"] = request.build_absolute_uri(request.path) + "?page={0}".format(queryPage - 1)
    
    if (page.has_next()):
        response_data["next"] = request.build_absolute_uri(request.path) + "?page={0}".format(queryPage + 1)

def merge_posts(posts_qs, posts_to_add, sort=False):
    if (len(posts_to_add) == 0):
        return posts_qs
        
    results = []
    for post in posts_qs:
        results.append(post)
    for post in posts_to_add:
        results.append(post)

    if sort:
        results.sort(key=lambda x : x["published"] if isinstance(x, dict) else str(x.published), reverse=True)
        
    return results

def merge_posts_with_github_activity(posts_qs, github_activity):
    return merge_posts(posts_qs, github_activity, sort=True)

def get_images(postId):
    images = Posts.objects.filter(post_id=postId).exclude(contentType__contains="text")
    url = []
    host_url = get_host_url()
    for img in images:
        image_url = urljoin(host_url, "posts", str(img.id), "image")
        url.append(image_url)
    return url
