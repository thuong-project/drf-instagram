from rest_framework import serializers

from images.models import Image
from images.serializers import ImageSerializer
from .models import Post
from django.utils.translation import gettext_lazy as _


class PostSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'content', 'image_set', 'number_of_likes', 'number_of_comments', 'parent_post']

    def create(self, validated_data):
        images = []
        if "image_set" in validated_data:
            images = validated_data.pop('image_set')

        post = Post.objects.create(**validated_data)

        for image in images:
            Image.objects.create(post=post, **image)

        return post

    def update(self, post, validated_data):
        if "image_set" in validated_data:
            images = validated_data.pop('image_set')
            post.image_set.all().delete()
            for image in images:
                Image.objects.create(post=post, **image)
        instance = super().update(post, validated_data)
        return instance
