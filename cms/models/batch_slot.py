from django.core.exceptions import ValidationError
from django.db import models
from cms.tasks import generate_batch_times_task
from .abstracts import Slot
from .batch import Batch

class BatchSlot(Slot):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='slots')

    def clean(self):
        super().clean()

        instructor = self.batch.instructor

        instructor_slots = instructor.slots.filter(
            day=self.day,
            start_time__lte=self.start_time,
            end_time__gte=self.end_time,
        )

        if not instructor_slots.exists():
            available_slots = instructor.slots.filter(day=self.day).order_by('start_time')

            if available_slots.exists():
                slot_info = ", ".join(
                    f"{slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}"
                    for slot in available_slots
                )
                raise ValidationError(
                    f"Instructor is not available during {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}. "
                    f"Available slot(s) on {self.get_day_display()}: {slot_info}"
                )
            else:
                raise ValidationError(
                    f"Instructor has no availability on {self.get_day_display()}."
                )

        overlapping_slots = BatchSlot.objects.filter(
            batch__instructor=instructor,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if overlapping_slots.exists():
            raise ValidationError("This batch has a conflicting time slot.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        generate_batch_times_task.delay(self.id)

    def __str__(self):
        return f"{self.batch.code} | {self.day} | {self.start_time.strftime('%H:%M %p')} - {self.end_time.strftime('%H:%M %p')}"
