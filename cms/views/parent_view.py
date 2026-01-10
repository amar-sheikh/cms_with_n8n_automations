from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from cms.forms import ParentForm
from cms.models import Parent, Parent

class ParentListView(ListView):
    model = Parent
    template_name = 'parents/_list.html'
    context_object_name = 'parents'
    paginate_by = 40

class ParentCreateView(CreateView):
    model = Parent
    template_name = 'parents/_form.html'
    form_class = ParentForm
    success_url = reverse_lazy('parents')

class ParentUpdateView(UpdateView):
    model = Parent
    template_name = 'parents/_form.html'
    form_class = ParentForm
    success_url = reverse_lazy('parents')

class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'parents/_confirm_delete.html'
    success_url = reverse_lazy('parents')
    context_object_name = 'student'
