from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Patient

# Decorate all Patient management views with @login_required
@method_decorator(login_required, name='dispatch')
class PatientListView(ListView):
    """List all patient records."""
    model = Patient
    template_name = 'pharmacy_app/patient_list.html'
    context_object_name = 'patients'

@method_decorator(login_required, name='dispatch')
class PatientDetailView(DetailView):
    """View details of a specific patient."""
    model = Patient
    template_name = 'pharmacy_app/patient_detail.html'
    context_object_name = 'patient'

@method_decorator(login_required, name='dispatch')
class PatientCreateView(CreateView):
    """Create a new patient record."""
    model = Patient
    template_name = 'pharmacy_app/patient_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'nhs_number', 
              'phone_number', 'address', 'known_allergies', 'current_medications']

    def form_valid(self, form):
        # Automatically set the user creating the record
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PatientUpdateView(UpdateView):
    """Update an existing patient record."""
    model = Patient
    template_name = 'pharmacy_app/patient_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'nhs_number', 
              'phone_number', 'address', 'known_allergies', 'current_medications']

@method_decorator(login_required, name='dispatch')
class PatientDeleteView(DeleteView):
    """Confirm and delete a patient record."""
    model = Patient
    template_name = 'pharmacy_app/confirm_delete.html'
    # Redirect to the patient list after successful deletion
    # Note: No namespace prefix needed for reverse_lazy
    success_url = reverse_lazy('patient_list')