from django import forms
from cms.models import Parent, Student
from .abstracts import BaseUserForm

class StudentForm(BaseUserForm):
    parent = forms.ModelChoiceField(queryset=Parent.objects.all())

    class Meta:
        model = Student
        fields = BaseUserForm.Meta.fields + ['status', 'dob', 'parent']
