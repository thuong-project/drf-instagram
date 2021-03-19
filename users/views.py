from rest_framework import viewsets
from rest_framework.decorators import action

from .models import User, UserProfile
from .access_policy import UserProfileAccessPolicy
from .serializers import UserSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserProfileAccessPolicy,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False)
    def me(self, request):
        me = request.user
        serializer = self.get_serializer(me)
        return Response(serializer.data)
