from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from cms.forms import CourseForm
from cms.models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'courses/_list.html'
    context_object_name = 'courses'
    paginate_by = 40

class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/_form.html'
    form_class=CourseForm
    success_url = reverse_lazy('courses')

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/_form.html'
    form_class=CourseForm
    success_url = reverse_lazy('courses')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/_confirm_delete.html'
    success_url = reverse_lazy('courses')
    context_object_name = 'batch'
