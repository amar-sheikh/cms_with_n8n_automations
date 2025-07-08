from django.db import models
from .image import Image

class Course(models.Model):
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255, null= False, blank=False)
    description = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title
