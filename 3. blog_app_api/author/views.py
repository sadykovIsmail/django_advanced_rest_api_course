from rest_framework import viewsets, views
from .models import AuthorModel, BlogPostModel
from .serializers import AuthorSerializer, BlogPostSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AuthorViews(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    def get_queryset(self):
        return AuthorModel.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogPostViews(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPostModel.objects.all()

    def get_queryset(self):
        # Only return posts of the logged-in user
        return BlogPostModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)
