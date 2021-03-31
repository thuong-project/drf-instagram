from django.db.models import F
from django.shortcuts import render
from rest_framework import generics, mixins

# Create your views here.
from comments.models import Comment
from likes.access_policys import LikeAccessPolicy
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.models import Post
from rest_framework import viewsets


class LikeView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = (LikeAccessPolicy,)

    def get_queryset(self):
        qs = Like.objects.all()
        if 'post_pk' in self.kwargs:
            qs = qs.filter(post_id=self.kwargs['user_pk'])
        if 'comment_pk' in self.kwargs:
            qs = qs.filter(comment_id=self.kwargs['comment_pk'])

        return qs

    def perform_create(self, serializer):
        add = dict(user_id=self.request.user.id)
        if 'post_pk' in self.kwargs:
            add['post_id'] = int(self.kwargs['post_pk'])
            Post.objects.filter(id=add['post_id']).update(number_of_likes=F('number_of_likes') + 1)
        if 'comment_pk' in self.kwargs:
            add['comment_id'] = int(self.kwargs['comment_pk'])
            Comment.objects.filter(id=add['comment_id']).update(number_of_likes=F('number_of_likes') + 1)
        serializer.save(**add)

    def perform_destroy(self, instance):
        Post.objects.filter(id=instance.post_id).update(number_of_comments=F('number_of_likes')-1)
        Comment.objects.filter(id=instance.comment_id).update(number_of_comments=F('number_of_likes') - 1)
        instance.delete()
