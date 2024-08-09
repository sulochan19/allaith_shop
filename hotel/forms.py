from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email', 'required':'true','type':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'required':'true'}))
    confirmpass = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repeat Password', 'required':'true'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmpass']

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        confirm_pass = cleaned_data.get('confirmpass')
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists")

        if password != confirm_pass:
            raise forms.ValidationError(
                "Password and confirm password does not matches"
            )