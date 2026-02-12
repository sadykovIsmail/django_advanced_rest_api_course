from rest_framework import serializers  # imports serializer
from .models import Task # imports from model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'quantity', 'completed', 'created_at'] # fields that will be seen by user
        read_only_fields = ['id', 'created_at', 'completed'] # read only ones