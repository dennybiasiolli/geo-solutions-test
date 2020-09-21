import threading
from django.db import models
from django.db.models import F
from django.db.models.functions import Power, Sqrt


NEAREST = 'nearest'
FURTHEST = 'furthest'
COORDINATE_CHOICES = (
    (NEAREST, 'Nearest'),
    (FURTHEST, 'Furthest'),
)


class Coordinate(models.Model):
    id_orig = models.IntegerField(unique=True)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return '{0}, {1}'.format(self.x, self.y)


class CoordinatesRequest(models.Model):
    owner = models.ForeignKey('auth.User',
                              related_name='coordinates_requests',
                              on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    n = models.IntegerField()
    operation = models.CharField(max_length=8, choices=COORDINATE_CHOICES)
    coordinates = models.ManyToManyField(Coordinate, blank=True)

    def __str__(self):
        return '{0} {1} to ({2}, {3})'.format(
            self.n, self.operation, self.x, self.y)

    def calc_points(self):
        qs = Coordinate.objects.annotate(
            distance=Sqrt(Power((F('x')-self.x), 2) + Power((F('y')-self.y), 2))
        ).order_by(
            '{0}distance'.format('-' if self.operation == FURTHEST else '')
        )[:self.n]
        for coordinate in qs:
            # TODO: not requested, but we can improve coordinates relationship
            # adding "distance" field, already computed
            self.coordinates.add(coordinate)

    def save(self, *args, **kwargs):
        should_calc_points = False
        if not self.pk:
            should_calc_points = True
        super(CoordinatesRequest, self).save(*args, **kwargs)
        if should_calc_points:
            self.calc_points()
