from .serializers import NotesSerializer, CategorySerializer, TagSerializer
from rest_framework import viewsets
from .models import Note, Category, Tag

class CategoryViewSet(viewsets.ModelViewSet):
    """End points of category"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class NotesViewSet(viewsets.ModelViewSet):
    """End points of API"""
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    # give the proper serializer
    def get_serializer_class(self):
        if self.action == "upload-image":
           return NotesSerializer
        return self.serializer_class

    




class TagsViewSet(viewsets.ModelViewSet):
    """End point of API"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
