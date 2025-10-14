"""
PharmaLogProject URL Configuration.
The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Import all views directly from your application
from pharmacy_app import views 

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    
    # Built-in authentication URLs (login, logout, password change, etc.)
    path('', include('django.contrib.auth.urls')), 
    
    # Home page URL
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # --- Application URLs (Patient CRUD) ---

    # Patient List View (Index)
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    
    # Patient Detail View
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    
    # Patient Create View
    path('patients/new/', views.PatientCreateView.as_view(), name='patient_create'),
    
    # Patient Update View
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    
    # Patient Delete View
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
]