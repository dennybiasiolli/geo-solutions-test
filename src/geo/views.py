from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from .models import CoordinatesRequest
from .serializers import CoordinatesRequestSerializer


class CoordinatesRequestViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    queryset = CoordinatesRequest.objects.all()
    serializer_class = CoordinatesRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
