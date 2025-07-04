from django.contrib import admin
from cms.models import Student, Batch

class BatchListFilter(admin.SimpleListFilter):
    title = "By Batch"
    parameter_name = 'batch_id'

    def lookups(self, request, model_admin):
        batch_list = []
        for batch in Batch.objects.all():
            batch_list.append((batch.id, batch.code))
        return batch_list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(batches__id__in = [self.value()])
        return queryset

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_filter = [ 'status', BatchListFilter ]
    list_display = [ 'full_name', 'parent', 'status', 'dob'  ]
    list_display_links = [ 'full_name', 'parent']

    @admin.display(description='Full name')
    def full_name(self, student):
        return str(student)
