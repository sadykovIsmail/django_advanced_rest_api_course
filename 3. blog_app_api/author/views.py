from rest_framework import viewsets, views
from .models import AuthorModel, BlogPostModel
from .serializers import AuthorSerializer, BlogPostSerializer
from rest_framework.permissions import AllowAny

class AuthorViews(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    permission_classes = [AllowAny]

class BlogPostViews(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
    permission_classes = [AllowAny]