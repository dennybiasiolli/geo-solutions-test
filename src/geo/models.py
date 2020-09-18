from django.db import models


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
