from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email', 'required':'true','type':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'required':'true'}))
    confirmpass = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repeat Password', 'required':'true'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact', 'required':'true'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmpass']

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        confirm_pass = cleaned_data.get('confirmpass')

        if password != confirm_pass:
            raise forms.ValidationError(
                "Password and confirm password does not match"
            )