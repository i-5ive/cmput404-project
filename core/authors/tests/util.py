
from core.authors.models import Author
from core.users.models import User

def setupUser(username):
    user = User.objects.create(username=username)
    return Author.objects.get(user=user)
