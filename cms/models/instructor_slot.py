from django.db import models
from .abstracts.slot import Slot
from .instructor import Instructor

class InstructorSlot(Slot):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='slots')
