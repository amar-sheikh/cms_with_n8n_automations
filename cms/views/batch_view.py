from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cms.forms import BatchForm, BatchSlotCreateFormSet, BatchSlotUpdateFormSet
from cms.models import Batch

class BatchListView(ListView):
    model = Batch
    template_name = 'batches/_list.html'
    context_object_name = 'batches'
    paginate_by = 40

class BatchCreateView(CreateView):
    template_name = 'batches/_form.html'

    def get(self, request):
        batch_form = BatchForm()
        slot_formset = BatchSlotCreateFormSet(prefix='slot_formset')
        return render(request, self.template_name, {
            'form': batch_form,
            'slot_formset': slot_formset
        })

    def post(self, request):
        batch_form = BatchForm(request.POST)
        if batch_form.is_valid():
            batch = batch_form.save()
            slot_formset = BatchSlotCreateFormSet(request.POST, instance=batch, prefix='slot_formset')
            if slot_formset.is_valid():
                slot_formset.save()
                return redirect('batches')
        else:
            slot_formset = BatchSlotCreateFormSet(request.POST, prefix='slot_formset')

        return render(request, self.template_name, {
            'form': batch_form,
            'slot_formset': slot_formset
        })

class BatchUpdateView(UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'batches/_form.html'

    def get(self, request, pk):
        batch = self.get_object()
        batch_form = BatchForm(instance=batch)
        slot_formset = BatchSlotUpdateFormSet(instance=batch, prefix='slot_formset')
        return render(request, self.template_name, {
            'form': batch_form,
            'slot_formset': slot_formset
        })

    def post(self, request, pk):
        batch = self.get_object()
        batch_form = BatchForm(request.POST, instance=batch)
        slot_formset = BatchSlotUpdateFormSet(request.POST, instance=batch, prefix='slot_formset')
        if batch_form.is_valid() and slot_formset.is_valid():
            batch = batch_form.save()
            slot_formset.save()
            return redirect('batches')
        return render(request, self.template_name, {
            'form': batch_form,
            'slot_formset': slot_formset
        })

class BatchDeleteView(DeleteView):
    model = Batch
    template_name = 'batches/_confirm_delete.html'
    success_url = reverse_lazy('batches')
    context_object_name = 'batch'
