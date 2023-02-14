from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django import forms


class AuthenticationForm(BaseAuthenticationForm):

    username = PhoneNumberField(
        widget=forms.TextInput(attrs={"autofocus": True})
    )