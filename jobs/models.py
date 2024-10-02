from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

# Create your models here.

#user model
class CustomUser(AbstractUser):
    CANDIDATE = 'candidate'
    EMPLOYER = 'employer'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CANDIDATE, 'Candidate'),
        (EMPLOYER, 'Employer'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_group',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permission',
        blank=True
    )

    def __str__(self):
        return f'{self.username} ({self.role})'



#model of company
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'employer'}
    )
    website = models.URLField(blank=True, null=True)
    company_size = models.IntegerField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.owner.role != 'employer':
            raise ValidationError("Owner must be an employer.")
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    

#job listing model
class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} at {self.company.name}'
    


#candidate job application model
class JobApplication(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey('JobListing', on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'candidate'}
    )
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'{self.candidate} applied for {self.job.title}'