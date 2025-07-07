from django.contrib.auth import get_user_model
from django import forms

class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

def save(self, commit=True):
        instance = super().save(commit=False)
        user = getattr(instance, 'user', None)
        if user is None:
            user = get_user_model().objects.create(username=self.cleaned_data['email'])

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        instance.user = user
        if commit:
            instance.save()

        return instance
