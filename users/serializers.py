from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import UserProfile, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'address']


class UserSerializer(WritableNestedModelSerializer):

    userprofile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userprofile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if 'userprofile' not in validated_data:
            validated_data['userprofile'] = UserProfile()
        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            del validated_data['username']
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
