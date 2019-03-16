from core.posts.models import Posts

from core.authors.util import get_author_url
from core.authors.models import Author, Follow

from core.users.models import User

def setupUser(username, password="", approve=True):
    user = User.objects.create(username=username)
    if password:
        user.set_password(password)
        user.save()

    author = Author.objects.get(user=user)
    if approve:
        author.approved = True
        author.save()
    return author

def createPostForAuthor(author, postContent, visibility="PUBLIC",  makeVisibleTo=[], unlisted=False):
    post = Posts.objects.create(
        author=author,
        contentType="text/plain",
        content=postContent,
        unlisted=unlisted,
        visibility=visibility,
        visibleTo=makeVisibleTo
    )
    post.save()
    return post

def makeFriends(author1, author2):
    Follow.objects.create(
        follower=get_author_url(str(author1.pk)),
        followed=get_author_url(str(author2.pk))
    )
    Follow.objects.create(
        follower=get_author_url(str(author2.pk)),
        followed=get_author_url(str(author1.pk))
    )