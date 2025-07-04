from django.db import models
from .abstracts.slot import Slot
from .batch import Batch

class BatchSlot(Slot):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='slots')
