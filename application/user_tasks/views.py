
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Type

from . import serializers
from .models import UserTask


class UserTaskListFilter(filters.FilterSet):
    finished = filters.BooleanFilter()

    class Meta:
        model = UserTask
        fields = ['finished']


class UserTasksViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'uuid'
    serializer_class = serializers.UserTaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    pagination_class = None

    def get_queryset(self):
        if self.request is None:
            return UserTask.objects.none()

        if getattr(self, "swagger_fake_view", False):
            return UserTask.objects.none()

        return UserTask.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        match self.action:
            case 'list' | 'create' | 'destroy':
                serializer_class = serializers.UserTaskSerializer
            case 'finish':
                serializer_class = serializers.FinishUserTaskSerializer
            case 'resume':
                serializer_class = serializers.ResumeUserTaskSerializer
            case _:
                serializer_class = None

        return serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @property
    def filterset_class(self) -> Type[filters.FilterSet] | None:
        match self.action:
            case 'list':
                filterset_class = UserTaskListFilter
            case _:
                filterset_class = None

        return filterset_class

    @action(detail=True, methods=['PUT'])
    def finish(self, request, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer_class()(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, methods=['PUT'])
    def resume(self, request, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer_class()(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
