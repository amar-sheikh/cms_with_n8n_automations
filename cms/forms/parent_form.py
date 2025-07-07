from cms.models import Parent
from .abstracts import BaseUserForm

class ParentForm(BaseUserForm):
    class Meta:
        model = Parent
        fields = BaseUserForm.Meta.fields + ['status', 'dob']
