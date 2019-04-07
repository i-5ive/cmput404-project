from rest_framework import serializers

from core.posts.models import Posts, Comments
from core.posts.util import get_images
from core.authors.serializers import get_summary, get_author_summary_from_url
from core.hostUtil import get_host_url, is_external_host

PAGE_SIZE = 5

class PostsSerializer(serializers.ModelSerializer):
    visibleTo = serializers.ListField(child=serializers.URLField(), default=list)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(default=list)

    class Meta:
        model = Posts
        fields = ('title', 'source', 'origin', 'description', 'contentType', 'content', 'author',
            'categories', 'count', 'size', 'next', 'comments', 'published', 'id', 'visibility',
            'visibleTo', 'unlisted', 'post_id', 'images')

    def get_count(self, instance):
        return instance.comments.count()
    
    def get_size(self, instance):
        return PAGE_SIZE

    def get_next(self, instance):
        return "{}/posts/{}/comments".format(get_host_url(), instance.id)
    
    def get_images(self, instance):
        return get_images(instance.post_id)

    # Credits to Ivan Semochkin, https://stackoverflow.com/a/41261614
    def to_representation(self, instance):
        representation = super(PostsSerializer, self).to_representation(instance)
        # From https://docs.djangoproject.com/en/dev/topics/db/queries/#limiting-querysets
        representation['comments'] = CommentsSerializer(instance.comments.all().order_by('-published')[:PAGE_SIZE], many=True, read_only=True).data
        representation['author'] = get_summary(instance.author)
        # TODO: integration with other servers
        if (not instance.origin):
            representation["origin"] = get_host_url() + "/posts/" + str(instance.id)
        if (not instance.source):
            representation["source"] = representation["origin"]
        del representation["post_id"]
        return representation 
        # Credit to Soufiaane and Tomas Walch for this: https://stackoverflow.com/a/35026359
    def create_temporary(self, data):
        return Posts(**data)

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('author', 'comment', 'contentType', 'published', 'id')

    # Credits to Ivan Semochkin, https://stackoverflow.com/a/41261614
    def to_representation(self, instance):
        representation = super(CommentsSerializer, self).to_representation(instance)
        representation['author'] = get_author_summary_from_url(instance.author)
        return representation