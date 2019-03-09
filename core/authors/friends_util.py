from core.authors.models import Follow

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