from django.contrib.auth.models import User
from django.test import TestCase
from unittest import mock

from geo.models import Coordinate, CoordinatesRequest


class MockedTestCase(TestCase):
    @mock.patch('geo.models.CoordinatesRequest.calc_points')
    def setUp(self, calc_points):
        self.user1 = User.objects.create_user(
            'user1', 'user1@email.it', 'user1')
        self.user2 = User.objects.create_user(
            'user2', 'user2@email.it', 'user2')

        Coordinate.objects.create(id=1, id_orig=0, x=917651.7, y=790243.0)
        Coordinate.objects.create(id=2, id_orig=1, x=886078.6, y=589230.7)
        Coordinate.objects.create(id=3, id_orig=2, x=349045.0, y=1022970.7)
        Coordinate.objects.create(id=4, id_orig=3, x=551877.0, y=1325102.2)
        Coordinate.objects.create(id=5, id_orig=4, x=893970.3, y=1292735.6)
        Coordinate.objects.create(id=6, id_orig=5, x=1190306.7, y=869297.9)
        Coordinate.objects.create(id=7, id_orig=6, x=1062606.1, y=1422169.1)
        Coordinate.objects.create(id=8, id_orig=7, x=457288.9, y=766397.5)
        Coordinate.objects.create(id=9, id_orig=8, x=673234.1, y=673265.0)

        CoordinatesRequest.objects.create(
            owner=self.user1,
            x=893970.3, y=1325102.2, n=3,
            operation='nearest')
        CoordinatesRequest.objects.create(
            owner=self.user1,
            x=893970.3, y=1325102.2, n=2,
            operation='furthest')
        CoordinatesRequest.objects.create(
            owner=self.user2,
            x=893970.3, y=1325102.2, n=1,
            operation='nearest')
