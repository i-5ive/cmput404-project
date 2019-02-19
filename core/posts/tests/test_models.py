from django.test import TestCase

from core.posts.models import Posts, Comments
from core.authors.models import Author
from core.users.models import User


class PostsModelTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.u2 = User.objects.create(username='user2')

    def test_create_post(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'source': "http://www.chaitali.com/",
            'origin': "http://www.cry.com/",
            'author': Author.objects.get(user=self.u1.id)
        })
        self.assertIsNotNone(post)
    
    def test_add_comment(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'source': "http://www.chaitali.com/",
            'origin': "http://www.cry.com/",
            'author': Author.objects.get(user=self.u1.id)
        })
        self.assertFalse(post.comments.all().exists())

        comment = Comments.objects.create(**{
            'comment': 'Hello World',
            'post': Posts.objects.get(id=post.id),
            'author': Author.objects.get(user=self.u2.id)
        })

        self.assertIsNotNone(comment)
        self.assertTrue(post.comments.all().exists())


