from .models import AuthorModel, BlogPostModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer"""
    user_name = serializers.CharField(
        source='user.username',
        read_only=True,
    )
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'email', 'created_at', 'user', 'user_name']
        read_only_fields = ['id', 'created_at', 'user']



class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.name',
        read_only=True,
    )
    class Meta:
        model = BlogPostModel
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
        
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = ['id', "image"]
        read_only_fields = ["id"]