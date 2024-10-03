from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import JobListingFilter, JobApplicationFilter

# Create your views here.


# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": CustomUserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

# Retrieve Role View
class RoleView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"role": user.role})
    


#permission for employers and admins
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'employer' or request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.company.owner == request.user
    

#function for manaaging company
class CompanyDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]


#list and create jobs
class JobListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobListingFilter 
    search_fields = ['title', 'company__name', 'location']
    ordering_fields = ['salary', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'employer':
            return JobListing.objects.filter(company__owner=user)
        
        if user.role == 'admin':
            return JobListing.objects.all()
        
        return JobListing.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'employer':
            raise PermissionDenied("Only employers can create job listings.")
        
        company = Company.objects.filter(owner=user).first()
        if not company:
            raise PermissionDenied("Employer must have a registered company.")
        
        serializer.save(company=company)



#retrieve, update, and delete jobs
class JobListingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]

    def perform_update(self, serializer):
        user = self.request.user
        job_listing = self.get_object()
        
        if job_listing.company.owner != user and user.role != 'admin':
            raise PermissionDenied("You do not have permission to update this job listing.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.company.owner != user and user.role != 'admin':
            raise PermissionDenied("You do not have permission to delete this job listing.")
        instance.delete()



#permission for Employers and Admins
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'employer' or request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.job.company.owner == request.user



#permission for Candidates
class IsCandidateOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'candidate' or request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.candidate == request.user



#list and create job applications
class JobApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobApplicationFilter
    search_fields = ['job__title', 'candidate__username']
    ordering_fields = ['applied_at', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return JobApplication.objects.filter(candidate=user)
        elif user.role == 'employer':
            return JobApplication.objects.filter(job__company__owner=user)
        elif user.role == 'admin':
            return JobApplication.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'candidate':
            raise PermissionDenied("Only candidates can apply for jobs.")
        
        serializer.save(candidate=user)



#retrieve, update, and delete job applications
class JobApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidateOrAdmin]

    def perform_update(self, serializer):
        user = self.request.user
        job_application = self.get_object()
        
        if user.role == 'employer' and job_application.job.company.owner == user:
            serializer.save()
        elif user.role == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this job application.")

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.candidate != user and user.role != 'admin':
            raise PermissionDenied("You do not have permission to delete this job application.")
        instance.delete()