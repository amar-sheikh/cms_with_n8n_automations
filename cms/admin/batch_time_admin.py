from django.contrib import admin
from cms.models import BatchTime

@admin.register(BatchTime)
class BatchTimeAdmin(admin.ModelAdmin):
    list_display = [
        'batch_code',
        'slot_day',
        'start_time',
        'end_time',
        'duration',
        'notified',
    ]
    list_filter = ['batch__code', 'notified']
    search_fields = ['batch__code']

    @admin.display(description='Batch')
    def batch_code(self, obj):
        return obj.batch.code

    @admin.display(description='Day')
    def slot_day(self, obj):
        return obj.start_datetime.strftime('%A')

    def start_time(self, obj):
        return obj.start_datetime.strftime('%Y-%m-%d %I:%M %p')

    def end_time(self, obj):
        return obj.end_datetime.strftime('%Y-%m-%d %I:%M %p')

    def duration(self, obj):
        total_minutes = int((obj.end_datetime - obj.start_datetime).total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}h {minutes}m"
