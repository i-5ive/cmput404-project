from rest_framework import serializers

from core.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # Inspired from https://stackoverflow.com/a/29867704 - cpury 2019/02/06
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']

        user.set_password(validated_data['password'])
        user.save()

        return user
