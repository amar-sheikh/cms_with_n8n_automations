from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255, null= False, blank=False)
    description = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title
