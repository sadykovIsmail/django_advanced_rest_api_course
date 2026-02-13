from .serializers import NotesSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Note, Category

class CategoryViewSet(viewsets.ModelViewSet):
    """End points of category"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny]

class NotesViewSet(viewsets.ModelViewSet):
    """End points of API"""
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    permission_classes = [AllowAny]
