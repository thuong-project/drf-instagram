from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user_id', 'post_id', 'comment_id']
