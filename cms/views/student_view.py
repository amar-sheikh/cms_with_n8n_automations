from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from cms.forms import StudentForm
from cms.models import Parent, Student

class StudentListView(ListView):
    model = Student
    template_name = 'students/_list.html'
    context_object_name = 'students'
    paginate_by = 40

class StudentCreateView(CreateView):
    model = Student
    template_name = 'students/_form.html'
    form_class = StudentForm
    success_url = reverse_lazy('students')

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/_form.html'
    form_class = StudentForm
    success_url = reverse_lazy('students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = Parent.objects.all()
        return context

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/_confirm_delete.html'
    success_url = reverse_lazy('students')
    context_object_name = 'student'
