from rest_framework import serializers

from .models import User
from django.utils.translation import gettext_lazy as _


class UserFullInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address', 'password', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            raise serializers.ValidationError({"username": _("Username can not change")})
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


class UserSomeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'avatar']
