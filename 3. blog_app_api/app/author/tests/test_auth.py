from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

AUTHOR_LIST_URL = reverse("authormodel-list")
POST_LIST_URL = reverse("blogpostmodel-list")

class AuthTests(TestCase):
    def test_endpoint_author_requires_login(self):
        client = APIClient()
        res = client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_endpoint_post_requires_login(self):
        client = APIClient()
        res = client.get(POST_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
