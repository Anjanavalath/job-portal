from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm # The one we created earlier with roles 
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1. Save the user
            user = form.save()
            
            # 2. Log them in immediately
            login(request, user)
            
            # 3. Check group and redirect accordingly
            if user.groups.filter(name="Student").exists():
                return redirect('application:student_dashboard')
            elif user.groups.filter(name="Company").exists():
                return redirect('core:company_dashboard')
            
            # Fallback to home if no group is found
            return redirect('core:home')
    else:
        form = RegisterForm()
    
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # --- Logic to redirect based on Group ---
            if user.groups.filter(name="Student").exists():
                return redirect('application:student_dashboard')
            elif user.groups.filter(name="Company").exists():
                return redirect('core:company_dashboard')
            else:
                return redirect('core:home') # Fallback if no group assigned
    else:
        form = AuthenticationForm()
    
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "users/logout.html")