'''Here we can connect to database'''

from django.db import models  #imports models
from django.core.validators import MinValueValidator, MaxValueValidator #imports validators
from django.conf import settings


class Task(models.Model):
    title = models.CharField(max_length=255) # title in the database with max 255 chars
    description = models.TextField(blank=True) # description will be created in db
    completed = models.BooleanField(default=False) # will be default incomplete
    created_at = models.DateTimeField(auto_now_add=True) # gives dates created not updated
    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
