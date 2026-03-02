import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import AuthorModel, BlogPostModel

User = get_user_model()


# ─────────────────────────────────────────────
# Helper functions — reusable shortcuts
# ─────────────────────────────────────────────

def create_user(username="testuser", password="testpass123"):
    return User.objects.create_user(username=username, password=password)


def create_author(user, name="Test Author", email="author@test.com"):
    return AuthorModel.objects.create(user=user, name=name, email=email)


def create_post(user, author, title="Test Post", content="Test content"):
    return BlogPostModel.objects.create(
        user=user, author=author, title=title, content=content
    )


# ─────────────────────────────────────────────
# URL names produced by DefaultRouter:
#   router.register('author', AuthorViews)
#     → 'authormodel-list'
#     → 'authormodel-detail'
#
#   router.register('posts', BlogPostViews)
#     → 'blogpostmodel-list'
#     → 'blogpostmodel-detail'
#     → 'blogpostmodel-upload-image'  (custom action)
# ─────────────────────────────────────────────

AUTHOR_LIST_URL = reverse("authormodel-list")
POST_LIST_URL = reverse("blogpostmodel-list")


# ═════════════════════════════════════════════
# AUTHOR TESTS
# ═════════════════════════════════════════════

class AuthorViewsTests(TestCase):
    """Tests for the /api/author/ endpoints."""

    def setUp(self):
        """
        setUp runs BEFORE every single test method.
        Here we create a fresh APIClient and a logged-in user.
        """
        self.client = APIClient()
        self.user = create_user()
        # force_authenticate skips JWT — it directly sets the user on the request.
        # This is the recommended way to authenticate in tests.
        self.client.force_authenticate(user=self.user)

    # ── Authentication ──────────────────────

    def test_unauthenticated_request_returns_401(self):
        """A client with no token should be rejected."""
        unauthenticated_client = APIClient()  # no force_authenticate
        res = unauthenticated_client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── Create ──────────────────────────────

    def test_create_author_success(self):
        """POST /api/author/ creates a new author owned by the logged-in user."""
        payload = {"name": "John Doe", "email": "john@example.com"}
        res = self.client.post(AUTHOR_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "John Doe")
        self.assertEqual(res.data["email"], "john@example.com")

        # verify the author was actually saved in the DB
        author = AuthorModel.objects.get(id=res.data["id"])
        self.assertEqual(author.user, self.user)

    def test_create_author_missing_name_returns_400(self):
        """POST without required field should return 400."""
        payload = {"email": "john@example.com"}  # 'name' is missing
        res = self.client.post(AUTHOR_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List ────────────────────────────────

    def test_list_returns_only_own_authors(self):
        """
        GET /api/author/ must return only THIS user's authors,
        not authors belonging to other users.
        """
        other_user = create_user(username="other")
        create_author(self.user, name="My Author")
        create_author(other_user, name="Their Author", email="other@test.com")

        res = self.client.get(AUTHOR_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "My Author")

    def test_list_empty_when_no_authors(self):
        """GET returns an empty list if the user has no authors yet."""
        res = self.client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    # ── Retrieve ────────────────────────────

    def test_retrieve_author(self):
        """GET /api/author/<id>/ returns the correct author."""
        author = create_author(self.user)
        url = reverse("authormodel-detail", args=[author.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], author.name)
        self.assertEqual(res.data["email"], author.email)

    # ── Update ──────────────────────────────

    def test_partial_update_author(self):
        """PATCH /api/author/<id>/ updates only the provided fields."""
        author = create_author(self.user)
        url = reverse("authormodel-detail", args=[author.id])

        res = self.client.patch(url, {"name": "Updated Name"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()  # reload from DB to see the saved value
        self.assertEqual(author.name, "Updated Name")

    def test_full_update_author(self):
        """PUT /api/author/<id>/ replaces all fields."""
        author = create_author(self.user)
        url = reverse("authormodel-detail", args=[author.id])
        payload = {"name": "New Name", "email": "new@example.com"}

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.name, "New Name")
        self.assertEqual(author.email, "new@example.com")

    # ── Delete ──────────────────────────────

    def test_delete_author(self):
        """DELETE /api/author/<id>/ removes the author from the DB."""
        author = create_author(self.user)
        url = reverse("authormodel-detail", args=[author.id])

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists
        self.assertFalse(AuthorModel.objects.filter(id=author.id).exists())


# ═════════════════════════════════════════════
# BLOG POST TESTS
# ═════════════════════════════════════════════

class BlogPostViewsTests(TestCase):
    """Tests for the /api/posts/ endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)
        # Every post needs an author
        self.author = create_author(self.user)

    # ── Authentication ──────────────────────

    def test_unauthenticated_request_returns_401(self):
        unauthenticated_client = APIClient()
        res = unauthenticated_client.get(POST_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── Create ──────────────────────────────

    def test_create_post_success(self):
        """POST /api/posts/ creates a post and auto-assigns the user."""
        payload = {
            "title": "My First Post",
            "content": "Hello World",
            "author": self.author.id,
        }
        res = self.client.post(POST_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "My First Post")

        # user must be auto-assigned (not sent in payload)
        post = BlogPostModel.objects.get(id=res.data["id"])
        self.assertEqual(post.user, self.user)

    def test_create_post_missing_title_returns_400(self):
        payload = {"content": "No title here", "author": self.author.id}
        res = self.client.post(POST_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List ────────────────────────────────

    def test_list_returns_only_own_posts(self):
        """Users must not see each other's posts."""
        other_user = create_user(username="other")
        other_author = create_author(other_user, name="Other", email="o@o.com")

        create_post(self.user, self.author, title="My Post")
        create_post(other_user, other_author, title="Their Post")

        res = self.client.get(POST_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "My Post")

    # ── Retrieve ────────────────────────────

    def test_retrieve_post(self):
        post = create_post(self.user, self.author)
        url = reverse("blogpostmodel-detail", args=[post.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], post.title)

    # ── Update ──────────────────────────────

    def test_partial_update_post(self):
        post = create_post(self.user, self.author)
        url = reverse("blogpostmodel-detail", args=[post.id])

        res = self.client.patch(url, {"title": "Updated Title"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")

    # ── Delete ──────────────────────────────

    def test_delete_post(self):
        post = create_post(self.user, self.author)
        url = reverse("blogpostmodel-detail", args=[post.id])

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPostModel.objects.filter(id=post.id).exists())

    # ── Image Upload ────────────────────────

    def test_upload_image_success(self):
        """
        POST /api/posts/<id>/upload-image/ with a real image file.
        tempfile creates a temporary file that auto-deletes when the block exits.
        Pillow (PIL) creates a real image so Django's ImageField validation passes.
        """
        post = create_post(self.user, self.author)
        url = reverse("blogpostmodel-upload-image", args=[post.id])

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))      # 10x10 pixel black image
            img.save(image_file, format="JPEG")
            image_file.seek(0)                    # rewind so Django can read it

            res = self.client.post(url, {"image": image_file}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertTrue(post.image)  # image field is now populated

    def test_upload_non_image_returns_400(self):
        """Sending a text file instead of an image should be rejected."""
        post = create_post(self.user, self.author)
        url = reverse("blogpostmodel-upload-image", args=[post.id])

        with tempfile.NamedTemporaryFile(suffix=".txt") as fake_file:
            fake_file.write(b"this is not an image")
            fake_file.seek(0)
            res = self.client.post(url, {"image": fake_file}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
