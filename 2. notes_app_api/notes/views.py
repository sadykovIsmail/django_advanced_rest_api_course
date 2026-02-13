from .serializers import NotesSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Note

class NotesViewSet(viewsets.ModelViewSet):
    """End points of API"""
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    permission_classes = [AllowAny]
