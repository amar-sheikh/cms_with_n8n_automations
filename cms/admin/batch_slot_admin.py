from django.contrib import admin
from datetime import datetime, timedelta
from cms.models import BatchTime, BatchSlot

@admin.register(BatchSlot)
class BatchSlotAdmin(admin.ModelAdmin):
    list_display = ['batch', 'day', 'start_time', 'end_time', 'remaining_classes']

    @admin.display(description='Remaining Classes')
    def remaining_classes(self, batch_slot):
        return batch_slot.times.filter(notified=False).count()
