from .models import AuthorModel, BlogPostModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source='user.username',
        read_only=True,
    )
    """Serializer"""
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'email', 'created_at', 'user', 'user_name']
        read_only = ['id', 'created_at', 'user', 'user_name']




class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.name',
        read_only=True,
    )
    class Meta:
        model = BlogPostModel
        fields = ['id', 'title', 'content', 'author', 'author_name', 'created_at', 'updated_at', 'user']
        read_only = ['id', 'created_at', 'author', 'author_name', 'user']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = ['id', "image"]
        read_only = ["id"]