from .views import NotesViewSet, CategoryViewSet, TagsViewSet
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notes', NotesViewSet, basename='note')
router.register('categories', CategoryViewSet)
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
