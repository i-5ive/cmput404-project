from rest_framework import serializers

from core.posts.models import Posts, Comments

class PostsSerializer(serializers.ModelSerializer):
    visibleTo = serializers.ListField(child=serializers.CharField(max_length=100), default=list)

    class Meta:
        model = Posts
        fields = ('id', 'post_id', 'author', 'source', 'origin', 'contentType', 'unlisted',
            'content', 'title', 'description', 'published', 'visibleTo', 'visibility', "categories")

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('post', 'author', 'contentType', 'id', 'comment', 'published')

