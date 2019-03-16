from rest_framework import serializers

from core.posts.models import Posts, Comments
from core.authors.serializers import get_summary
from core.hostUtil import get_host_url

class PostsSerializer(serializers.ModelSerializer):
    visibleTo = serializers.ListField(child=serializers.URLField(), default=list)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ('id', 'post_id', 'author', 'contentType', 'source', 'origin', 'unlisted', 'comments',
            'content', 'title', 'description', 'published', 'visibleTo', 'visibility', "categories")

    # Credits to Ivan Semochkin, https://stackoverflow.com/questions/41248271/django-rest-framework-not-responding-to-read-only-on-nested-data
    def to_representation(self, instance):
        representation = super(PostsSerializer, self).to_representation(instance)
        representation['author'] = get_summary(instance.author)
        # TODO: integration with other servers
        if (not instance.origin):
            representation["origin"] = get_host_url() + "/posts/" + str(instance.id)
        if (not instance.source):
            representation["source"] = representation["origin"]
        return representation 

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('contentType', 'id', 'comment', 'published')

    def to_representation(self, instance):
        representation = super(CommentsSerializer, self).to_representation(instance)
        representation['author'] = get_summary(instance.author)
        return representation
