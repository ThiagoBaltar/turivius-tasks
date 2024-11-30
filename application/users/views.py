
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, TokenSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request is None:
            return User.objects.none()

        if getattr(self, "swagger_fake_view", False):
            return User.objects.none()

        return User.objects.all()

    def get_permissions(self):
        match self.action:
            case 'create':
                permission_classes = [AllowAny]
            case _:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'key'
    serializer_class = TokenSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.auth

    def get_queryset(self):
        if self.request is None:
            return Token.objects.none()

        if getattr(self, "swagger_fake_view", False):
            return Token.objects.none()

        return Token.objects.filter(user=self.request.user)

    def get_permissions(self):
        match self.action:
            case 'create':
                permission_classes = [AllowAny]
            case 'logout':
                permission_classes = [IsAuthenticated]
            case _:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['DELETE'])
    def logout(self, request, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
