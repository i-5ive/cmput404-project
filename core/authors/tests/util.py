
from core.authors.models import Author
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
