from django.db import models
from .abstracts.base_user import BaseUser
from .parent import Parent

class Student(BaseUser):
    parent = models.ForeignKey(Parent, on_delete=models.PROTECT, related_name='children')
