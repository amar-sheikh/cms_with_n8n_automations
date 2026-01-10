from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cms.forms import InstructorForm, InstructorSlotCreateFormSet, InstructorSlotUpdateFormSet
from cms.models import Instructor

class InstructorListView(ListView):
    model = Instructor
    template_name = 'instructors/_list.html'
    context_object_name = 'instructors'
    paginate_by = 40

class InstructorCreateView(CreateView):
    template_name = 'instructors/_form.html'

    def get(self, request):
        instructor_form = InstructorForm()
        slot_formset = InstructorSlotCreateFormSet(prefix='slot_formset')
        return render(request, self.template_name, {
            'form': instructor_form,
            'slot_formset': slot_formset
        })

    def post(self, request):
        with atomic():
            instructor_form = InstructorForm(request.POST)
            if instructor_form.is_valid():
                instructor = instructor_form.save()
                slot_formset = InstructorSlotCreateFormSet(request.POST, instance=instructor, prefix='slot_formset')
                if slot_formset.is_valid():
                    try:
                        slot_formset.save()
                        return redirect('instructors')
                    except ValidationError as e:
                        slot_formset._non_form_errors = slot_formset.non_form_errors() + e.error_list
            else:
                slot_formset = InstructorSlotCreateFormSet(request.POST, prefix='slot_formset')

        return render(request, self.template_name, {
            'form': instructor_form,
            'slot_formset': slot_formset
        })

class InstructorUpdateView(UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'instructors/_form.html'

    def get(self, request, pk):
        instructor = self.get_object()
        instructor_form = InstructorForm(instance=instructor)
        slot_formset = InstructorSlotUpdateFormSet(instance=instructor, prefix='slot_formset')
        return render(request, self.template_name, {
            'form': instructor_form,
            'slot_formset': slot_formset
        })

    def post(self, request, pk):
        instructor = self.get_object()
        instructor_form = InstructorForm(request.POST, instance=instructor)
        slot_formset = InstructorSlotUpdateFormSet(request.POST, instance=instructor, prefix='slot_formset')

        if instructor_form.is_valid() and slot_formset.is_valid():
            instructor = instructor_form.save()
            slot_formset.save()
            return redirect('instructors')
        return render(request, self.template_name, {
            'form': instructor_form,
            'slot_formset': slot_formset
        })

class InstructorDeleteView(DeleteView):
    model = Instructor
    template_name = 'instructors/_confirm_delete.html'
    success_url = reverse_lazy('instructors')
    context_object_name = 'batch'
