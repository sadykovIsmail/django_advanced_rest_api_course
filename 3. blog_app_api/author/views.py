from rest_framework import viewsets, views
from .models import AuthorModel, BlogPostModel
from .serializers import AuthorSerializer, BlogPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class AuthorViews(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get_queryset(self):
        return AuthorModel.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogPostViews(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()
