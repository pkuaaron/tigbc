from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField


class SignupForm(UserCreationForm):
    email = EmailField(max_length=200, required=True, help_text='电子邮箱')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
