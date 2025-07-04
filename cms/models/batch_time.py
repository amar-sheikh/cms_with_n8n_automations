from django.db import models
from .batch_slot import Batch, BatchSlot

class BatchTime(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    batch_slot = models.ForeignKey(BatchSlot, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.batch.code} | {self.batch_slot}'

    class Meta:
        ordering = ['start_datetime']
