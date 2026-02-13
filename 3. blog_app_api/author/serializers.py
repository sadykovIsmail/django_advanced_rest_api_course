from .models import AuthorModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer"""
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'email', 'created_at']
        read_only = ['id', 'created_at']
        