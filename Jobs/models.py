from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')


    def __str__(self):
        return self.title
    
class Application(models.Model):
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=50, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


    def __str__(self):
        return f"{self.user_id.username} - {self.job_id.title}"
    
