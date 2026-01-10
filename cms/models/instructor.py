from django.db import models
from .abstracts.base_user import BaseUser

class Instructor(BaseUser):
    language = models.CharField(max_length=150)
