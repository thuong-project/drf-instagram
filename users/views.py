from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .access_policy import UserAccessPolicy
from .models import User
from .serializers import UserFullInfoSerializer, UserSomeInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserAccessPolicy,)
    serializer_class = UserFullInfoSerializer
    queryset = User.objects.all()

    @action(detail=False)
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    def retrieve(self, request, *args, **kwargs):
        if request.user == self.get_object() or request.user.groups.filter(name='admin').exists():
            return Response(UserFullInfoSerializer(self.get_object()).data)
        else:
            return Response(UserSomeInfoSerializer(self.get_object()).data)
