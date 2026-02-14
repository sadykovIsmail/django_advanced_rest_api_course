from rest_framework import serializers  # imports serializer
from .models import Task # imports from model

class TaskSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source='user.username',
        read_only = True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'quantity', 'completed', 'created_at', 'user', 'user_name'] # fields that will be seen by user
        read_only_fields = ['id', 'created_at', 'completed', 'user', 'user_name'] # read only ones

