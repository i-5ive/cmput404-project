from rest_framework import serializers

from core.posts.models import Posts, Comments

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('post_id', 'author', 'source_url', 'origin_url', 'content_type', 
            'text_content','image_content', 'title', 'description', 'published_time')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('post', 'author', 'content_type', 'id', 'comment', 'published_time')
