from django.db import models
from django.contrib.auth.models import User

# Model for patient records
class Patient(models.Model):
    # Basic Demographics
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nhs_number = models.CharField(max_length=10, unique=True, help_text="Unique Identifier")
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Medical Information
    known_allergies = models.TextField(blank=True, help_text="List known drug and food allergies.")
    current_medications = models.TextField(blank=True, help_text="List active prescriptions and OTC medications.")
    # Current diagnosis to relate to medications
    current_diagnosis = models.TextField(blank=True, help_text="Brief summary of current diagnosis or clinical notes.")
    
    # Record metadata (useful for tracking who created the record)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Track last modification
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_patients', editable=False)
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = "Patients"
        permissions = [
            ("change_patient_medications", "Can change patient medications"),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (NHS: {self.nhs_number})"

    def get_absolute_url(self):
        # Defines the URL to redirect to after a successful creation/update
        from django.urls import reverse
        # No namespace prefix 'pharmacy_app:' is needed here
        return reverse('patient_detail', kwargs={'pk': self.pk})