from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
from users.models import User
from .access_policys import CommentAccessPolicy
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (CommentAccessPolicy,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.all()
        if 'post_pk' in self.kwargs:
            qs = qs.filter(post_id=self.kwargs['user_pk'])
        if 'comment_pk' in self.kwargs:
            qs = qs.filter(parent_comment_id=self.kwargs['comment_pk'])

        return qs

    def perform_create(self, serializer):
        add = dict(user_id=self.request.user.id)
        if 'post_pk' in self.kwargs:
            add['post_id'] = int(self.kwargs['post_pk'])
            Post.objects.filter(id=add['post_id']).update(number_of_comments=F('number_of_comments')+1)
        if 'comment_pk' in self.kwargs:
            add['parent_comment_id'] = int(self.kwargs['comment_pk'])
            Comment.objects.filter(id=add['parent_comment_id']).update(number_of_comments=F('number_of_comments') + 1)
        serializer.save(**add)

    def perform_destroy(self, instance):
        Post.objects.filter(id=instance.post_id).update(number_of_comments=F('number_of_comments')-1)
        Comment.objects.filter(id=instance.parent_comment_id).update(number_of_comments=F('number_of_comments') - 1)
        instance.delete()