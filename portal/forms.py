from django import forms
from django.contrib.auth.models import User
from .models import AccessCode

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    access_code = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")

        try:
            code = AccessCode.objects.get(
                code=cleaned_data['access_code'],
                is_used=False
            )
        except:
            raise forms.ValidationError("Invalid or used code")

        cleaned_data['code_obj'] = code
        return cleaned_data