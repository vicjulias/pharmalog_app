from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# type: ignore
from pharmacy_app.models import Patient


class Command(BaseCommand):
    help = 'Create roles and assign permissions: Admin, Pharmacist, Pharmacy Technician, Pharmacy Assistant'

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Patient)

        # Collect the model permissions. Use filter().first() to
        # avoid raising exceptions when checking which permissions exist.
        perms = {}
        for codename in ['add_patient', 'change_patient', 'delete_patient', 'view_patient', 'change_patient_medications']:
            p = Permission.objects.filter(content_type=ct, codename=codename).first()
            if p:
                perms[codename] = p
            else:
                # keep messages simple to avoid static analysis on self.style
                self.stdout.write(f'Permission {codename} not found.')

        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        pharmacist_group, _ = Group.objects.get_or_create(name='Pharmacist')
        technician_group, _ = Group.objects.get_or_create(name='Pharmacy Technician')
        assistant_group, _ = Group.objects.get_or_create(name='Pharmacy Assistant')

        # Assign permissions
        # Admin: all patient perms
        admin_perms = [p for k, p in perms.items() if p]
        admin_group.permissions.set(admin_perms)

        # Pharmacist: manage patients (add, change, view, delete)
        pharmacist_group.permissions.set([perms.get('add_patient'), perms.get('change_patient'), perms.get('view_patient'), perms.get('delete_patient')])

        # Pharmacy Technician: view and change medications
        technician_group.permissions.set([perms.get('view_patient'), perms.get('change_patient_medications')])

        # Pharmacy Assistant: view only
        assistant_group.permissions.set([perms.get('view_patient')])

        # Final success message
        self.stdout.write('Roles created/updated.')
