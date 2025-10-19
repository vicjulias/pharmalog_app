from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Patient
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegisterForm

# Add "login required" to all Patient management views
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
              'phone_number', 'address', 'known_allergies', 'current_medications', 'current_diagnosis']

    def form_valid(self, form):
        # Automatically set the user creating the record
        form.instance.created_by = self.request.user
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PatientUpdateView(UpdateView):
    """Update an existing patient record."""
    model = Patient
    template_name = 'pharmacy_app/patient_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'nhs_number', 
              'phone_number', 'address', 'known_allergies', 'current_medications', 'current_diagnosis']

    def form_valid(self, form):
        # Record who last modified the patient
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If user is in Pharmacy Technician group (or has only medication permission), limit fields
        if self.request.user.groups.filter(name='Pharmacy Technician').exists() and not self.request.user.has_perm('pharmacy_app.change_patient'):
            # Only allow editing medications
            for field_name in list(form.fields.keys()):
                if field_name != 'current_medications':
                    form.fields.pop(field_name, None)
        return form

@method_decorator(login_required, name='dispatch')
class PatientDeleteView(DeleteView):
    """Confirm and delete a patient record."""
    model = Patient
    template_name = 'pharmacy_app/confirm_delete.html'
    # Redirect to the patient list after successful deletion.
    # No namespace prefix is required here; the URL name is global in this app.
    success_url = reverse_lazy('patient_list')


def register(request):
    """Allow new users to register."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign default group so new users have view-only access
            try:
                default_group = Group.objects.get(name='Pharmacy Assistant')
                user.groups.add(default_group)
            except ObjectDoesNotExist:
                # If the group isn't created, continue without failing; admin can assign later
                pass
            # Log the user in after registering
            messages.success(request, 'Account created. You have been assigned view-only access. An administrator can grant additional permissions.')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})