from .models import Note, Category
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
        fields = ['id', 'title', 'content', 'category', 'created_at']
        read_only = ['id', 'created_at']
