from uuid import uuid4
from django.db import models


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    file = models.ImageField(max_length=100, upload_to="picture")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
