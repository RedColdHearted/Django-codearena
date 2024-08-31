from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserUpdateForm(forms.ModelForm):
    """Form for update user data."""

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
        )
