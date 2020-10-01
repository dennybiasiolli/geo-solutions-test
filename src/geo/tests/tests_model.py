from unittest import mock
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate

from geo.models import Coordinate, CoordinatesRequest
from .mocked_data import MockedTestCase


class CoordinateModelTestCase(MockedTestCase):
    def test_model(self):
        c = Coordinate(x=1.3, y=2.4)
        self.assertEqual(str(c), '1.3, 2.4')


class CoordinatesRequestModelTestCase(MockedTestCase):
    @mock.patch('geo.models.CoordinatesRequest.calc_points')
    def test_model(self, calc_points):
        cr = CoordinatesRequest.objects.create(
            owner=self.user1,
            x=1.3, y=2.4, n=7,
            operation='nearest',
        )
        self.assertEqual(str(cr), '7 nearest to (1.3, 2.4)')
        calc_points.assert_called_once_with()
        cr.n = 1
        cr.save()
        calc_points.assert_called_once_with()
