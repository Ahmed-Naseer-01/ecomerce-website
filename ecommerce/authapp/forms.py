from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Invalid username or password. Please try again.',
    }

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email','phone_number']

        
class user_detail(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email','phone_number']