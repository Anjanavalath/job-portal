from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'cv']
        widgets = {
            
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email Address',
                'class': 'form-control'
            }),
          
        }