from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from datetime import datetime, timedelta
from calendar import monthrange, day_abbr
from collections import defaultdict
from cms.models import BatchTime, Batch, Student, Parent

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

def get_upcoming_batches(request):
    batch_times = BatchTime.objects.filter(
        start_datetime__gte=timezone.now(),
        start_datetime__lt=timezone.now() + timedelta(minutes=30),
        notified=False
    ).select_related('batch')

    batches = Batch.objects.filter(times__in=batch_times)
    students = Student.objects.filter(batches__in=batches).distinct()
    parents = Parent.objects.filter(children__in=students, status='active').distinct()

    parents_data = []
    for parent in parents:
        parent_data = {
            'id': parent.id,
            'name': str(parent),
            'email': parent.user.email,
            'dob': parent.dob,
        }

        children_data = []
        for child in parent.children.filter(id__in=students, status='active'):
            child_data = {
                'id': child.id,
                'name': str(child),
                'email': child.user.email,
                'status': child.status,
                'dob': child.dob,
            }

            child_batches_data = []
            for batch in child.batches.filter(id__in=batches):
                batch_time = batch.times.filter(id__in=batch_times).first()
                child_batches_data.append({
                    'id': batch.id,
                    'code': batch.code,
                    'start_time': batch_time.start_datetime.strftime('%I:%M %p'),
                    'end_time': batch_time.start_datetime.strftime('%I:%M %p'),
                    'color': batch.color,
                    'course': batch.course.title,
                    'instructor': str(batch.instructor),
                })

            child_data['batches'] = child_batches_data
            children_data.append(child_data)

        parent_data['children'] = children_data
        parents_data.append(parent_data)

    batches_data = []
    for batch in batches:
        batch_time = batch.times.filter(id__in=batch_times).first()
        batches_data.append({
            'id': batch.id,
            'code': batch.code,
            'start_time': batch_time.start_datetime,
            'end_time': batch_time.start_datetime,
            'color': batch.color,
            'course': batch.course.title,
            'instructor': str(batch.instructor),
            'instructor_email': batch.instructor.user.email,
            'parents_emails': list(
                parents.filter(children__in=batch.students.all())
                .distinct()
                .values_list('user__email', flat=True)
            ),
            'students_emails': list(batch.students.values_list('user__email'))
        })

    return JsonResponse({
        'parents': parents_data,
        'batches': batches_data
    })

@csrf_exempt
def mark_notified(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            batches = data.get('batches', [])
            for batch in batches:
                BatchTime.objects.filter(
                    batch__id=batch.get('id'),
                    start_datetime=batch.get('start_time'),
                    end_datetime=batch.get('end_time')
                ).update(notified=True)

            return JsonResponse({'message': 'Successfully updated'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
