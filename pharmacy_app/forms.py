from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Simple registration form without email field."""
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
