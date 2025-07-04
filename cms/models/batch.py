from django.db import models
from .course import Course
from .instructor import Instructor
from .student import Student

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='batches')
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, related_name='batches')
    students = models.ManyToManyField(Student, related_name='batches')

    code = models.CharField(max_length=255, unique=True, null=False, blank=False)
    meeting_url = models.URLField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    color = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Batches'
        ordering = ['start_date']
