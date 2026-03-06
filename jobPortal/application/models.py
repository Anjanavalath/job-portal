from django.db import models
from django.contrib.auth.models import User
from core.models import Job

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    cv = models.FileField(upload_to='cvs/') 
    applied_at = models.DateTimeField(auto_now_add=True)
    

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"
