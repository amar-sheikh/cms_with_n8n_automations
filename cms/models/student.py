from django.core.exceptions import ValidationError
from django.db import models
from .abstracts.base_user import BaseUser
from .parent import Parent

class Student(BaseUser):
    parent = models.ForeignKey(Parent, on_delete=models.PROTECT, related_name='children')

    def clean(self):
            super().clean()

            if self.parent and self.dob <= self.parent.dob:
                raise ValidationError("Student's date of birth must be after parent's date of birth.")
