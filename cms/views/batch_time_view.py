from django.views.generic import ListView
from cms.models import BatchTime
from datetime import datetime, timedelta
from collections import defaultdict
from calendar import monthrange, day_abbr

class BatchTimeListView(ListView):
    model = BatchTime
    template_name = 'batch_times/_list.html'
    context_object_name = 'batch_times'
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view = self.request.GET.get('view', 'week')
        offset = int(self.request.GET.get('offset', 0))

        today = datetime.today().date()
        context['today'] = today

        if view == 'month':
            first_of_this_month = today.replace(day=1)
            target_month_date = first_of_this_month + timedelta(days=offset * 30)
            start_of_month = target_month_date.replace(day=1)

            _, days_in_month = monthrange(start_of_month.year, start_of_month.month)
            month_days = [start_of_month + timedelta(days=i) for i in range(days_in_month)]

            start_weekday = start_of_month.weekday()
            leading_blanks = [''] * start_weekday

            full_days = leading_blanks + month_days
            while len(full_days) % 7 != 0:
                full_days.append('')

            weeks = [full_days[i:i + 7] for i in range(0, len(full_days), 7)]

            context['month_weeks'] = weeks
            context['day_names'] = list(day_abbr)
        else:
            if view == 'day':
                context['days'] = [today + timedelta(days=offset)]
            else:
                start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
                context['days'] = [start_of_week + timedelta(days=i) for i in range(7)]

            context['grouped_day_slots'] = self._generate_grouped_slots(context['days'])

        context['view'] = view
        context['offset'] = offset

        return context

    def _generate_grouped_slots(self, days):
        grouped = defaultdict(list)

        for day in days:
            start_time = datetime.combine(day, datetime.strptime("00:00", "%H:%M").time())
            slots = [start_time + timedelta(minutes=15 * i) for i in range(96)]
            for i in range(0, 96, 4):
                hour_label = slots[i].strftime("%I %p")
                grouped[hour_label].append(slots[i:i+4])

        return grouped.items()
