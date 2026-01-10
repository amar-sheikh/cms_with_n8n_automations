from django.contrib.auth import get_user_model
from django import forms
from cms.models import BatchSlot, BatchTime, Batch, Instructor, Course, Student
from datetime import datetime, timedelta

class BatchForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all())
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    class Meta:
        model = Batch
        fields = ['code', 'meeting_url', 'course', 'instructor', 'students', 'start_date', 'end_date', 'color' ]

BatchSlotCreateFormSet = forms.inlineformset_factory(
    Batch,
    BatchSlot,
    fields=['day', 'start_time', 'end_time'],
    extra=1,
    can_delete=True
)

BatchSlotUpdateFormSet = forms.inlineformset_factory(
    Batch,
    BatchSlot,
    fields=['day', 'start_time', 'end_time'],
    extra=0,
    can_delete=True
)
