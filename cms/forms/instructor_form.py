from django import forms
from cms.models import Instructor, InstructorSlot
from .abstracts import BaseUserForm

class InstructorForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = Instructor
        fields = BaseUserForm.Meta.fields + ['language', 'status', 'dob']

    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'language', 'status', 'dob']

InstructorSlotCreateFormSet = forms.inlineformset_factory(
    Instructor,
    InstructorSlot,
    fields=['day', 'start_time', 'end_time'],
    extra=1,
    can_delete=True
)

InstructorSlotUpdateFormSet = forms.inlineformset_factory(
    Instructor,
    InstructorSlot,
    fields=['day', 'start_time', 'end_time'],
    extra=0,
    can_delete=True
)
