from .serializers import NotesSerializer, CategorySerializer, TagSerializer, NoteImageSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Note, Category, Tag
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'image_upload':
            return NoteImageSerializer
        return self.serializer_class

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {'type': 'string', 'format': 'binary'}
                },
                'required': ['image'],
            }
        }
    )
    @action(
        methods=['POST'],
        detail=True,
        url_path='upload-image',
        parser_classes=[MultiPartParser, FormParser],
    )
    def image_upload(self, request, pk=None):
        note = self.get_object()
        serializer = self.get_serializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsViewSet(viewsets.ModelViewSet):
    """End point of API"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
