from core.authors.models import Follow
from core.authors.util import get_author_url

def get_friends_set(authorUrl):
    followers = Follow.objects.filter(followed=authorUrl).values()
    followed = Follow.objects.filter(follower=authorUrl).values()
    followersSet = set()
    followedSet = set()

    for follow in followers:
        followersSet.add(follow["follower"])
    for follow in followed:
        followedSet.add(follow["followed"])
    return followersSet.intersection(followedSet)

def get_friends(authorUrl):
    return list(get_friends_set(authorUrl))

# I'm upset this didn't exist before
def get_friends_from_pk(pk):
    pk = str(pk)
    return get_friends(get_author_url(pk))

def are_friends(authorUrlA, authorUrlB):
    f = Follow.objects.filter(follower=authorUrlA, followed=authorUrlB)
    if len(f) < 1:
        return False
    f = Follow.objects.filter(follower=authorUrlB, followed=authorUrlA)
    if len(f) < 1:
        return False
    return True, f