from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

# Create your tests here.


class TestOneEqualOne(APITestCase):

    def test_11(self):
        self.assertEqual(1, 1)

