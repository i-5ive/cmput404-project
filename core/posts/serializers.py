from rest_framework import serializers

from core.posts.models import Posts, Comments
from core.authors.serializers import AuthorSummarySerializer
from core.hostUtil import get_host_url
from core.authors.util import get_author_url

PAGE_SIZE = 50

class PostsSerializer(serializers.ModelSerializer):
    visibleTo = serializers.ListField(child=serializers.CharField(max_length=100), default=list)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ('title', 'source', 'origin', 'description', 'contentType', 'content', 'author',
            'categories', 'count', 'size', 'next', 'comments', 'published', 'id', 'visibility',
            'visibleTo', 'unlisted')

    def get_count(self, instance):
        return instance.comments.count()
    
    def get_size(self, instance):
        return PAGE_SIZE

    def get_next(self, instance):
        return "{}/posts/{}/comments".format(get_host_url(), instance.id)

    # Credits to Ivan Semochkin, https://stackoverflow.com/questions/41248271/django-rest-framework-not-responding-to-read-only-on-nested-data
    def to_representation(self, instance):
        representation = super(PostsSerializer, self).to_representation(instance)
        instance.author.host = get_host_url()
        instance.author.url = get_author_url(str(instance.author.id))
        representation['author'] = AuthorSummarySerializer(instance.author, read_only=True).data
        # From https://docs.djangoproject.com/en/dev/topics/db/queries/#limiting-querysets
        representation['comments'] = CommentsSerializer(instance.comments.all().order_by('-published')[:5], many=True, read_only=True).data
        return representation 

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('author', 'comment', 'contentType', 'published', 'id')

    # Credits to Ivan Semochkin, https://stackoverflow.com/questions/41248271/django-rest-framework-not-responding-to-read-only-on-nested-data
    def to_representation(self, instance):
        representation = super(CommentsSerializer, self).to_representation(instance)
        instance.author.host = get_host_url()
        instance.author.url = get_author_url(str(instance.author.id))
        representation['author'] = AuthorSummarySerializer(instance.author, read_only=True).data
        return representation 

