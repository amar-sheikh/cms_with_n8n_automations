from django.db import models
from .batch_slot import Batch, BatchSlot

class BatchTime(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='times')
    batch_slot = models.ForeignKey(BatchSlot, on_delete=models.CASCADE, related_name='times')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch.code} | {self.start_datetime.date()} | {self.start_datetime.strftime('%H:%M %p')} - {self.end_datetime.strftime('%H:%M %p')}"

    @property
    def duration(self):
        return self.end_datetime - self.start_datetime

    class Meta:
        ordering = ['start_datetime']
