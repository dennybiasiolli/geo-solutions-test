from rest_framework import serializers

from .models import Coordinate, CoordinatesRequest


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('id_orig', 'x', 'y')


class CoordinatesRequestSerializer(serializers.HyperlinkedModelSerializer):
    coordinates = CoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = CoordinatesRequest
        fields = ('id', 'x', 'y', 'n', 'operation', 'coordinates')
