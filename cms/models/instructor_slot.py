from django.core.exceptions import ValidationError
from django.db import models
from .abstracts import Slot
from .instructor import Instructor

class InstructorSlot(Slot):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='slots')

    def clean(self):
        super().clean()

        overlapping = InstructorSlot.objects.filter(
            instructor=self.instructor,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This instructor has a conflicting time slot.")
