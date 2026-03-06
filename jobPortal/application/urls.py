from django.urls import path
from . import views

app_name = "application"

urlpatterns = [
    path('job/<int:id>/', views.apply_job, name="apply_job"),
    path('my-applications/', views.student_dashboard, name="student_dashboard"),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]