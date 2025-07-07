from django import forms
from django.core.validators import validate_image_file_extension
import os
import requests
from cms.models import Image

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, validators=[validate_image_file_extension])

    class Meta:
        model = Image
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size = 10 * 1024 * 1024
            if image.size > max_size:
                raise forms.ValidationError(f'Image too large. Max size is 10 MB')
        return image

    def save(self, commit=True):
        image = self.cleaned_data.get('image')

        if not image:
            return super().save(commit=commit)

        instance = super().save(commit=False)
        old_file_id = instance.image_id
        instance.name = image.name
        try:
            file_url, file_id = self.upload_to_google_drive(image, old_file_id)
            instance.url = file_url
            instance.image_id = file_id
        except Exception as e:
            instance.url = None
            instance.image_id = None
            return None

        if commit:
            instance.save()
        return instance

    @staticmethod
    def upload_to_google_drive(image, old_file_id=None):
        response = requests.post(
            os.getenv('N8N_UPLOAD_IMAGE_GOOGLE_URL'),
            files={
                "file": (image.name, image.read(), image.content_type)
            },
            data={
                'oldFileId' : old_file_id.lstrip('=')
            }
        )
        response.raise_for_status()
        data = response.json()

        if data['status'] != 'success':
            raise ValueError("Unexpected response from n8n webhook")

        return data['fileUrl'], data['fileId']
