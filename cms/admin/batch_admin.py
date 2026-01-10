from django.utils import timezone
from django.contrib import admin
from datetime import datetime, timedelta
from cms.models import Batch, BatchSlot, BatchTime

class BatchStatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'batch_status'

    def lookups(self, request, model_admin):
        return [
            ('upcoming', 'Upcoming'),
            ('running', 'Running'),
            ('ended', 'Ended'),
        ]

    def queryset(self, request, queryset):
        today_date = timezone.now().date()
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today_date)
        elif self.value() == 'ended':
            return queryset.filter(end_date__lt=today_date)
        elif self.value() == 'running':
            return queryset.filter(start_date__lte=today_date, end_date__gte=today_date)
        return queryset

class BatchSlotTabularAdmin(admin.TabularInline):
    model = BatchSlot
    extra = 1

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_filter = [ BatchStatusFilter, 'course', 'instructor', ]
    list_display = [ 'code', 'instructor', 'meeting_url', 'status']
    inlines = [BatchSlotTabularAdmin]

    @admin.display(description='Status')
    def status(self, batch):
        today_date = timezone.now().date()
        if batch.start_date > today_date:
            return 'Upcomming'
        if batch.end_date < today_date:
            return 'Ended'
        return  'Running'
