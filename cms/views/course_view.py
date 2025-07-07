from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from cms.forms import CourseForm, ImageForm
from cms.models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'courses/_list.html'
    context_object_name = 'courses'
    paginate_by = 40

class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/_form.html'
    success_url = reverse_lazy('courses')

    def get(self, request, *args, **kwargs):
        course_form = CourseForm()
        image_form = ImageForm()
        return render(request, self.template_name, {
            'form': course_form,
            'image_form': image_form
        })

    def post(self, request, *args, **kwargs):
        course_form = CourseForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        if course_form.is_valid() and image_form.is_valid():
            course = course_form.save(commit=False)
            image = image_form.save()
            course.image = image
            course.save()
            return redirect('courses')

        return render(request, self.template_name, {
            'form': course_form,
            'image_form': image_form
        })

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/_form.html'
    form_class=CourseForm
    success_url = reverse_lazy('courses')

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        course_form = CourseForm(instance=course)
        image_form = ImageForm(instance=course.image)
        return render(request, self.template_name, {
            'form': course_form,
            'image_form': image_form
        })

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course_form = CourseForm(request.POST, instance=course)

        image_form = ImageForm(
            request.POST,
            request.FILES,
            instance=course.image if course.image else None
        )

        if course_form.is_valid() and image_form.is_valid():
            course = course_form.save(commit=False)

            if image_form.cleaned_data.get('image'):
                image = image_form.save()
                course.image = image

            course.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': course_form,
            'image_form': image_form
        })

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/_confirm_delete.html'
    success_url = reverse_lazy('courses')
    context_object_name = 'batch'
