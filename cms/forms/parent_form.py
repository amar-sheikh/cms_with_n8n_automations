from cms.models import Parent
from .abstracts import BaseUserForm

class ParentForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = Parent
        fields = BaseUserForm.Meta.fields + ['status', 'dob']

    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'email', 'status', 'dob']
