from .models import Note, Category, Tag
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """Category to front end"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only = ['id', 'created_at']

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'tags', 'created_at']
        read_only = ['id', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only = ['id']