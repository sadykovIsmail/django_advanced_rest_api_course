from django.db import models
from rest_framework.validators import AllowAny

# Create your models here.

class AuthorModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    