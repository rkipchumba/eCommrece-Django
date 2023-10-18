import email
import imp
from webbrowser import get
from django import forms
from django.contrib.auth import get_user_model

# from ecommerce.views import User

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Your Content'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError('Email has to be gmail.com')
        return email




    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password2 != password:
            raise forms.ValidationError('Passwords must match.')
        
        return cleaned_data