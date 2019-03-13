from rest_framework import serializers

from core.posts.models import Posts, Comments
from core.authors.serializers import AuthorSummarySerializer
from core.hostUtil import get_host_url
from core.authors.util import get_author_url

class PostsSerializer(serializers.ModelSerializer):
    visibleTo = serializers.ListField(child=serializers.CharField(max_length=100), default=list)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ('id', 'post_id', 'author', 'source', 'origin', 'contentType', 'unlisted', 'comments',
            'content', 'title', 'description', 'published', 'visibleTo', 'visibility', "categories")

    # Credits to Ivan Semochkin, https://stackoverflow.com/questions/41248271/django-rest-framework-not-responding-to-read-only-on-nested-data
    def to_representation(self, instance):
        representation = super(PostsSerializer, self).to_representation(instance)
        instance.author.host = get_host_url()
        instance.author.url = get_author_url(str(instance.author.id))
        representation['author'] = AuthorSummarySerializer(instance.author, read_only=True).data
        return representation 

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('post', 'author', 'contentType', 'id', 'comment', 'published')

