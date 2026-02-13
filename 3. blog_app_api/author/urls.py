from django.urls import path, include
from .models import AuthorModel
from rest_framework.routers import DefaultRouter
from .views import AuthorViews

router = DefaultRouter()
router.register('author', AuthorViews)

urlpatterns = [
    path('', include(router.urls))
]