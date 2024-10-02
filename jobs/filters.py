from django_filters import rest_framework as filters
from .models import JobListing, JobApplication
import django_filters


#job listing filter
class JobListingFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    salary = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = JobListing
        fields = ['location', 'salary', 'is_active']


#job application filter
class JobApplicationFilter(django_filters.FilterSet):
    job_title = django_filters.CharFilter(field_name='job__title', lookup_expr='icontains')
    candidate_username = django_filters.CharFilter(field_name='candidate__username', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=JobApplication.STATUS_CHOICES)

    class Meta:
        model = JobApplication
        fields = ['job_title', 'candidate_username', 'status']
