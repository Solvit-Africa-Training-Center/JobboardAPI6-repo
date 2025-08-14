from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.

class CustomuserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have email address')
        email= self.normalize_email[email]
        user= self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, passowrd=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('role', User.Role.ADMIN)

        return self.create_user(email,passowrd, **kwargs)
    
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN= 'ADMIN','Admin'
        RECRUITER= 'recruiter', 'Recruiter'
        CANDIDATE= 'Candidate', 'Candidate'

    email= models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    first_name=models.CharField(max_length=40)
    last_name= models.CharField(max_length=50)
    role=models.CharField(max_length=40, choices= Role.choices)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=True)

    objects=CustomuserManager()
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['first_name', 'last_name', 'password']

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class Job(models.Model):
    JOBTYPE=[
        ('Technology&IT','Technology&IT'),
        ('Engineering & Technical','Engineering & Technical'),
        ('Healthcare & Medical','Healthcare & Medical'),
        ('Education & Training','Education & Training'),
        ('Business & Finance','Business & Finance')
    ]
    JOBCATEGORY=[
        ('FullTime','FullTime'),
        ('PartTime','PartTime'),
        ('Internship', 'Internship'),
        
    ]

   
    title=models.CharField(max_length=40)
    description=models.TextField()
    requirements=models.TextField()
    company_name=models.CharField(max_length=40)
    location=models.CharField(max_length=100)
    Salary=models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    category=models.CharField(max_length=40  ,choices=JOBCATEGORY)
    job_type= models.CharField(max_length=30, choices=JOBTYPE)
    recruiter= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    created_at= models.DateTimeField(auto_now_add=True)
    deadline=models.DateTimeField(blank=True, null=False)
    
    def __str__(self):
        return self.title
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
   ]
    job=models.ForeignKey(Job, on_delete=models.CASCADE, related_name='application')
    candidate=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='application')
    cover_letter=models.TextField()
    cv=models.FileField(upload_to='resume/',null=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.candidate.email ->{self.job.title}"
    
class Userprofile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='profile')
    resume=models.FileField(upload_to='resume/', null=True, blank=True)
    bio=models.TextField(max_length=50, blank=True)
    def __str__(self):
        return f"Profile of {self.user.email}"
    
class SavedJob(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='save_job')
    job=models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_job')
    saved_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"




    



