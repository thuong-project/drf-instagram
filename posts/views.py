from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from .access_policys import PostAccessPolicy
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (PostAccessPolicy,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['user_pk'])

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs['user_pk'])
