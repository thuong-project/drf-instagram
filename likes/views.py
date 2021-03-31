from django.db.models import F
from django.shortcuts import render
from rest_framework import generics, mixins, status

# Create your views here.
from rest_framework.response import Response

from comments.models import Comment
from likes.access_policys import LikeAccessPolicy
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.models import Post
from rest_framework import viewsets


class LikeView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
               mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = (LikeAccessPolicy,)

    def get_queryset(self):
        qs = Like.objects.all()
        if 'post_pk' in self.kwargs:
            qs = qs.filter(post_id=self.kwargs['post_pk'])
        if 'comment_pk' in self.kwargs:
            qs = qs.filter(comment_id=self.kwargs['comment_pk'])

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if 'duplicate' in self.kwargs:
            return Response("duplicate", status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        add = dict(user_id=self.request.user.id)
        if 'post_pk' in self.kwargs:
            add['post_id'] = int(self.kwargs['post_pk'])
            if Like.objects.filter(user_id=add['user_id'], post_id=add['post_id']).exists():
                self.kwargs['duplicate'] = True
                return
            Post.objects.filter(id=add['post_id']).update(number_of_likes=F('number_of_likes') + 1)
        if 'comment_pk' in self.kwargs:
            add['comment_id'] = int(self.kwargs['comment_pk'])
            if Like.objects.filter(user_id=add['user_id'], comment_id=add['comment_id']).exists():
                self.kwargs['duplicate'] = True
                return
            Comment.objects.filter(id=add['comment_id']).update(number_of_likes=F('number_of_likes') + 1)
        serializer.save(**add)

    def perform_destroy(self, instance):
        Post.objects.filter(id=instance.post_id).update(number_of_comments=F('number_of_likes') - 1)
        Comment.objects.filter(id=instance.comment_id).update(number_of_comments=F('number_of_likes') - 1)
        instance.delete()
