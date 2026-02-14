from .serializers import NotesSerializer, CategorySerializer, TagSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Note, Category, Tag
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class CategoryViewSet(viewsets.ModelViewSet):
    """End points of category"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

class NotesViewSet(viewsets.ModelViewSet):
    """End points of API"""
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

class TagsViewSet(viewsets.ModelViewSet):
    """End point of API"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
