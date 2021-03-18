from rest_framework import viewsets

from .models import User, UserProfile
from .access_policy import UserProfileAccessPolicy
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserProfileAccessPolicy, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


