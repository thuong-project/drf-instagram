"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_nested import routers

from instagram import settings
from users import views as usersViews
from posts import views as postsViews
from comments import views as commentsViews
from likes import views as likesViews

router = routers.SimpleRouter()
router.register(r'users', usersViews.UserViewSet, basename="user")
router.register(r'posts', postsViews.PostViewSet, basename="post")
router.register(r'comments', commentsViews.CommentViewSet, basename="comment")
router.register(r'likes', likesViews.LikeView, basename="like")

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', postsViews.PostViewSet, basename='user-post')

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', commentsViews.CommentViewSet, basename='post-comment')
posts_router.register(r'likes', likesViews.LikeView, basename='post-like')

comments_router = routers.NestedSimpleRouter(router, r'comments', lookup='comment')
comments_router.register(r'comments', commentsViews.CommentViewSet, basename='comment-comment')
comments_router.register(r'likes', likesViews.LikeView, basename='comment-like')


api_urls = [
    path('', include(router.urls)),
    path('',include(users_router.urls)),
    path('',include(posts_router.urls)),
    path('',include(comments_router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf'))
]

urlpatterns = [
    path('api/', include(api_urls)),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
