from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name="home"),
    path('jobs/', views.jobs, name="jobs"),
    path('jobs/<int:id>/', views.job_detail, name="job_detail"),
    path('jobs/create/', views.create_job, name="create_job"),
    path('jobs/<int:id>/close/', views.close_job, name="close_job"),
    path('dashboard/company/', views.company_dashboard, name="company_dashboard"),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:app_id>/status/<str:status>/', views.update_application_status, name='update_status'),
]