from rest_framework import serializers

from core.authors.models import Author
from core.users.serializers import UserSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'github', 'bio', 'user')

    user = UserSerializer()

class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.URLField()
    host = serializers.URLField()
    id = serializers.URLField()

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url')