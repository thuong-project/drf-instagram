from rest_framework import serializers

from images.models import Image
from images.serializers import ImageSerializer
from .models import Comment
from django.utils.translation import gettext_lazy as _


class CommentSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'image_set', 'number_of_likes',
                  'number_of_comments', 'post_id', 'parent_comment_id', 'user_id']

    def create(self, validated_data):
        print(validated_data)
        images = []
        if "image_set" in validated_data:
            images = validated_data.pop('image_set')

        comment = Comment.objects.create(**validated_data)

        for image in images:
            Image.objects.create(comment=comment, **image)

        return comment

    def update(self, comment, validated_data):
        if "image_set" in validated_data:
            images = validated_data.pop('image_set')
            comment.image_set.all().delete()
            for image in images:
                Image.objects.create(post=comment, **image)
        instance = super().update(comment, validated_data)
        return instance
