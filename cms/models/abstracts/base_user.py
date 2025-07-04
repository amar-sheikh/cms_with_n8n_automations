from django.db import models
from django.contrib.auth import get_user_model

class BaseUser(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'In Active'),
        ('active', 'Active'),
        ('blocked', 'Blocked')
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    dob = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
