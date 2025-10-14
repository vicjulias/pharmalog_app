from django.contrib import admin
from .models import Patient

# Registery models:
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nhs_number', 'last_name', 'first_name', 'date_of_birth', 'created_by')
    search_fields = ('nhs_number', 'last_name', 'first_name')
    list_filter = ('created_at',)
    
    # Automatically set the created_by field to the currently logged-in user
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)