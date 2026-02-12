from rest_framework import viewsets # gives all CRUD operations
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """Api endpoint for tasks."""
    serializer_class = TaskSerializer
    queryset = Task.objects.all() # which tasks are available
    permission_classes = [AllowAny]