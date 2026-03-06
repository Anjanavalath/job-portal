# core/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Job description...'}),
        }