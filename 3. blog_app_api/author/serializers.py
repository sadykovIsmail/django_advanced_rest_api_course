from .models import AuthorModel, BlogPostModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer"""
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'email', 'created_at']
        read_only = ['id', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only = ['id', 'created_at']