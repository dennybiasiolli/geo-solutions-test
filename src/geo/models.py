from django.db import models


class Coordinate(models.Model):
    id_orig = models.IntegerField(unique=True)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return '{0}, {1}'.format(self.x, self.y)
