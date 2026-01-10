from django.contrib import admin
from cms.models import InstructorSlot

@admin.register(InstructorSlot)
class InstructorSlotAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'day', 'start_time', 'end_time']
