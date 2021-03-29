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
        qs = Post.objects
        if 'user_pk' in self.kwargs:
            qs = qs.filter(user=self.kwargs['user_pk'])
        return qs

    def perform_create(self, serializer):
        add = dict()
        if 'user_pk' in self.kwargs:
            add['user_id'] = self.kwargs['user_pk']
        else:
            add['user_id'] = self.request.user.id
        serializer.save(**add)
