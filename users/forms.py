from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "email"]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
