from django.test import TestCase


class CoordinatesRequestAPIUnauthenticatedTestCase(TestCase):
    def test_get(self):
        response = self.client.get('/coordinates-request/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.',
        })

    def test_post(self):
        response = self.client.post('/coordinates-request/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.',
        })
