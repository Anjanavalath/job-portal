from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Job
from .forms import JobForm
from application.models import Application

# --- Public Views ---

def home(request):
    return render(request, "core/home.html")

def jobs(request):
    # Filter for open jobs and order by newest first
    jobs_list = Job.objects.filter(status="open").order_by("-created_at")
    return render(request, "core/jobs.html", {"jobs": jobs_list})

def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, "core/job_detail.html", {"job": job})

# --- Employer Dashboard & Job Management ---

@login_required
def company_dashboard(request):
    if not request.user.groups.filter(name="Company").exists():
        return redirect('core:home')
    
    my_jobs = Job.objects.filter(company=request.user).order_by("-created_at")
    return render(request, "core/company_dashboard.html", {"jobs": my_jobs})

@login_required
def create_job(request):
    if not request.user.groups.filter(name="Company").exists():
        return redirect('core:home')

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user 
            job.status = 'open'
            job.save()
            messages.success(request, "Job posting created successfully!")
            return redirect('core:company_dashboard')
    else:
        form = JobForm()
    return render(request, "core/create_job.html", {"form": form})

@login_required
def close_job(request, id):
    job = get_object_or_404(Job, id=id, company=request.user)
    job.status = 'closed'
    job.save()
    messages.info(request, f"Job listing '{job.title}' has been closed.")
    return redirect('core:company_dashboard')

# --- Applicant Management ---

@login_required
def view_applicants(request, job_id):
    # Ensure the job belongs to the logged-in company
    job = get_object_or_404(Job, id=job_id, company=request.user)
    
    # Use 'applied_at' to match your Application model
    applicants = job.applications.all().order_by('-applied_at')
    
    return render(request, "core/view_applicants.html", {
        "job": job, 
        "applicants": applicants
    })

@login_required
def update_application_status(request, app_id, status):
    # Fetch the application ensuring it belongs to a job owned by this company
    application = get_object_or_404(Application, id=app_id, job__company=request.user)
    
    # LOGIC: If the application is already accepted, do not allow any changes
    if application.status == 'accepted':
        messages.warning(request, "This application has already been accepted and cannot be changed.")
        return redirect('core:view_applicants', job_id=application.job.id)

    if status in ['accepted', 'rejected']:
        application.status = status
        application.save()

        if status == 'accepted':
            subject = f"Application Update: {application.job.title}"
            message = f"""
Dear {application.full_name},

Congratulations! Your application for the position of "{application.job.title}" has been ACCEPTED by {application.job.company.username}.

The employer will contact you at this email address ({application.email}) for further interview details.

Best of luck,
The JobFlow Team
            """
            
            sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@jobflow.com')
            recipient_email = application.email 

            try:
                send_mail(
                    subject,
                    message,
                    sender_email,
                    [recipient_email],
                    fail_silently=False,
                )
                messages.success(request, f"Successfully accepted {application.full_name}. Confirmation email sent.")
            except Exception as e:
                # If mail fails, we still accepted them, but we notify the admin
                messages.error(request, "Application status updated, but notification email failed to send. Please check SMTP settings.")
                print(f"Email Error: {e}")
        
        elif status == 'rejected':
            messages.info(request, f"Application for {application.full_name} has been rejected.")

    return redirect('core:view_applicants', job_id=application.job.id)