from django.contrib import admin
from cms.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = [ 'language' ]
    list_display = [ 'title', 'description', 'language']
