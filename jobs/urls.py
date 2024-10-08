from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    #CustomUser
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('role/', RoleView.as_view(), name='role'),

    #adding compony
    path('company/add/', CompanyCreateView.as_view(), name='company-create'),

    #job listing
    path('jobs/', JobListingListCreateAPIView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobListingDetailAPIView.as_view(), name='job-detail'),

    #job applications
    path('applications/', JobApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('job-applications/<int:pk>/update-status/', UpdateJobApplicationStatusAPIView.as_view(), name='update-job-application-status'),
    path('applications/<int:pk>/', JobApplicationDetailAPIView.as_view(), name='application-detail'),
]
