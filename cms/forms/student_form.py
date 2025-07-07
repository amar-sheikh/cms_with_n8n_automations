from django import forms
from cms.models import Parent, Student
from .abstracts import BaseUserForm

class StudentForm(BaseUserForm):
    parent = forms.ModelChoiceField(queryset=Parent.objects.all())

    class Meta(BaseUserForm.Meta):
        model = Student
        fields = BaseUserForm.Meta.fields + ['status', 'dob', 'parent']

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'status', 'parent', 'dob']
