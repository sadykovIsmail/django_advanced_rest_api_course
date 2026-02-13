from .serializers import NotesSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Notes

class NotesViewSet(viewsets.ModelViewSet):
    """End points of API"""
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = [AllowAny]
