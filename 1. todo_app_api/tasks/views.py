from rest_framework import viewsets # gives all CRUD operations
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class TaskViewSet(viewsets.ModelViewSet):
    """Api endpoint for tasks."""
    serializer_class = TaskSerializer
    queryset = Task.objects.all() # which tasks are available
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)