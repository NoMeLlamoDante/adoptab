from django.db import models


# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100)
    file = models.ImageField(upload_to="media")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
