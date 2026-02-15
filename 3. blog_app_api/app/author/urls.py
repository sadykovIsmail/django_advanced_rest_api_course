from django.urls import path, include
from .models import AuthorModel
from rest_framework.routers import DefaultRouter
from .views import AuthorViews, BlogPostViews

router = DefaultRouter()
router.register('author', AuthorViews)
router.register('posts', BlogPostViews)

urlpatterns = [
    path('', include(router.urls))
]