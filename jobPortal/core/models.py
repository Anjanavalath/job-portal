from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    # Choices for the status field
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    exit

    
    def __str__(self):
        return f"{self.title} at {self.company.username}"