from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Job
from .models import Application
from .forms import ApplicationForm

# Specify the login_url so logged-out students are redirected to your custom login page
@login_required(login_url='users:login')

def apply_job(request, id):
    # 1. Security: Only allow users in the "Student" group to apply
    if not request.user.groups.filter(name="Student").exists():
        # If a Company tries to apply, send them back to the home page
        return redirect('core:home')

    job = get_object_or_404(Job, id=id, status="open")
    
    # 2. Logic: Prevent a student from applying to the same job twice
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('application:student_dashboard')

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            return redirect('application:student_dashboard')
    else:
        # Pre-fill the form with the student's email for better UX
        form = ApplicationForm(initial={'email': request.user.email})

    return render(request, "application/apply.html", {"form": form, "job": job})


@login_required(login_url='users:login')
def student_dashboard(request):
    # Security check: Ensure only students see this
    if not request.user.groups.filter(name="Student").exists():
        return redirect('core:home')
        
    # FIX: Changed 'created_at' to 'applied_at' to match your model
    my_apps = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    
    # Calculate counts for the dashboard stats
    total_apps = my_apps.count()
    accepted_apps = my_apps.filter(status='accepted').count()

    return render(request, "application/student_dashboard.html", {
        "applications": my_apps,
        "total_count": total_apps,
        "accepted_count": accepted_apps
    })

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES) # request.FILES is for the CV
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('application:student_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'application/apply.html', {'form': form, 'job': job})