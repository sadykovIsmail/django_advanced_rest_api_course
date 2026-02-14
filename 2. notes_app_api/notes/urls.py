from .views import NotesViewSet, CategoryViewSet, TagsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notes', NotesViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls))
]