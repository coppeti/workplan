from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthday', 'username']
        required_fields = ['first_name', 'last_name', 'email', 'birthday', 'username']



