from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("company", "Company"),
    )
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Register as")

    class Meta:
        model = User
        fields = ["username", "email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Logic to assign the Django Group
            role_selected = self.cleaned_data.get("role")
            group_name = "Student" if role_selected == "student" else "Company"
            
            # This ensures the group exists before adding the user
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
        return user