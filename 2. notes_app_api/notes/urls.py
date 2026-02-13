from .views import NotesViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notes', NotesViewSet)

urlpatterns = [
    path('', include(router.urls))
]