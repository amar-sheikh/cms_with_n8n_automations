from django import forms
from django.core.validators import validate_image_file_extension
from cms.models import Course

class CourseForm(forms.ModelForm):
    image = forms.ImageField(required=False, validators=[validate_image_file_extension])

    class Meta:
        model = Course
        fields = ['title', 'language', 'image', 'description']
