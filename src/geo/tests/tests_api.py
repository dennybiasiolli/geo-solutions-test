from unittest import mock
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate

from geo.models import CoordinatesRequest
from .mocked_data import MockedTestCase


class CoordinatesRequestAPITestCase(MockedTestCase):
    def setUp(self):
        super(CoordinatesRequestAPITestCase, self).setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_get(self):
        response = self.client.get('/coordinates-request/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_post_without_data(self):
        response = self.client.post('/coordinates-request/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            'x': ['This field is required.'],
            'y': ['This field is required.'],
            'n': ['This field is required.'],
            'operation': ['This field is required.'],
        })

    @mock.patch('geo.models.CoordinatesRequest.calc_points')
    def test_post_with_data(self, calc_points):
        response = self.client.post('/coordinates-request/', {
            'x': 306835.5,
            'y': 724232.6,
            'n': 5,
            'operation': 'nearest',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': 4,
            'x': 306835.5,
            'y': 724232.6,
            'n': 5,
            'operation': 'nearest',
            'coordinates': [],
        })
        calc_points.assert_called_once_with()

    def test_calc_points(self):
        req = CoordinatesRequest.objects.all()
        for r in req:
            self.assertEqual(r.coordinates.count(), 0)
            r.calc_points()
            self.assertEqual(r.coordinates.count(), r.n)

    def test_get_with_data_user1(self):
        req = CoordinatesRequest.objects.all()
        for r in req:
            r.calc_points()
        response = self.client.get('/coordinates-request/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/coordinates-request/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'x': 893970.3,
            'y': 1325102.2,
            'n': 3,
            'operation': 'nearest',
            'coordinates': [{
                'id_orig': 3,
                'x': 551877.0,
                'y': 1325102.2,
            }, {
                'id_orig': 4,
                'x': 893970.3,
                'y': 1292735.6,
            }, {
                'id_orig': 6,
                'x': 1062606.1,
                'y': 1422169.1,
            }]
        })

        response = self.client.get('/coordinates-request/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 2,
            'x': 893970.3,
            'y': 1325102.2,
            'n': 2,
            'operation': 'furthest',
            'coordinates': [{
                'id_orig': 1,
                'x': 886078.6,
                'y': 589230.7,
            }, {
                'id_orig': 7,
                'x': 457288.9,
                'y': 766397.5,
            }]
        })

        response = self.client.get('/coordinates-request/3/')
        self.assertEqual(response.status_code, 404)

    def test_get_with_data_user2(self):
        self.client.force_authenticate(user=self.user2)

        req = CoordinatesRequest.objects.all()
        for r in req:
            r.calc_points()
        response = self.client.get('/coordinates-request/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/coordinates-request/1/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/coordinates-request/2/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/coordinates-request/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 3,
            'x': 893970.3,
            'y': 1325102.2,
            'n': 1,
            'operation': 'nearest',
            'coordinates': [{
                'id_orig': 4,
                'x': 893970.3,
                'y': 1292735.6,
            }]
        })
