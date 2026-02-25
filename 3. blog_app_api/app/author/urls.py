from django.urls import path, include
from .models import AuthorModel
from rest_framework.routers import DefaultRouter
from .views import AuthorViews, BlogPostViews
from django.conf.urls.static import static
from django.conf import settings


router = DefaultRouter()
router.register('author', AuthorViews)
router.register('posts', BlogPostViews)

urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
