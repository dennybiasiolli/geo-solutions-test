from rest_framework import serializers

from .models import CoordinatesRequest


class CoordinatesRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoordinatesRequest
        fields = ('id', 'x', 'y', 'n', 'operation')
