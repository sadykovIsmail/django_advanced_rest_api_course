from django.db import models

# Create your models here.

class AuthorModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class BlogPostModel(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE) # foreing key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    