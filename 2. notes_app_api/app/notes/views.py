from .serializers import NotesSerializer, CategorySerializer, TagSerializer
from rest_framework import viewsets
from .models import Note, Category, Tag
from drf_spectacular.utils import extend_schema

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
    
    # extend drf schema
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "image": {"type": "string", "format": "binary"}
                },
                "required": ["image"],
            }
        }
    )





class TagsViewSet(viewsets.ModelViewSet):
    """End point of API"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
