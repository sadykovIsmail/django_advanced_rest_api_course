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


# ── URL names ────────────────────────────────────────────────────────
AUTHOR_LIST_URL = reverse("authormodel-list")
POST_LIST_URL   = reverse("blogpostmodel-list")


# ════════════════════════════════════════════════════════════════════
# AUTH TESTS
# ════════════════════════════════════════════════════════════════════

class AuthTests(TestCase):

    def test_author_endpoint_requires_login(self):
        client = APIClient()   # no user attached
        res = client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posts_endpoint_requires_login(self):
        client = APIClient()
        res = client.get(POST_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
