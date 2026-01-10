from django.contrib import admin
from cms.models import Parent

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_filter = [ 'status' ]
    list_display = [ 'full_name', 'user__email', 'status', 'dob'  ]
    list_display_links = [ 'full_name' ]

    @admin.display(description='Full name')
    def full_name(self, parent):
        return str(parent)
