import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import AuthorModel, BlogPostModel

User = get_user_model()


# ── Helpers ──────────────────────────────────────────────────────────
def create_user(username="testuser", password="testpass123"):
    return User.objects.create_user(username=username, password=password)

def create_author(user, name="Test Author", email="author@test.com"):
    return AuthorModel.objects.create(user=user, name=name, email=email)

def create_post(user, author, title="Test Post", content="Test content"):
    return BlogPostModel.objects.create(
        user=user, author=author, title=title, content=content
    )


# ════════════════════════════════════════════════════════════════════
# AUTH TESTS
# ════════════════════════════════════════════════════════════════════

class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author_list_url = reverse("authormodel-list")
        self.post_list_url   = reverse("blogpostmodel-list")

    def test_author_endpoint_requires_login(self):
        res = self.client.get(self.author_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posts_endpoint_requires_login(self):
        res = self.client.get(self.post_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
