from rest_framework import viewsets, views
from .models import AuthorModel
from .serializers import AuthorSerializer
from rest_framework.validators import AllowAny

class AuthorViews(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    permission_classes = [AllowAny]