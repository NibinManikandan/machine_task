from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


#users
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


#company 
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'description', 'owner', 'website', 'company_size', 'industry']



#jobs
class JobListingSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company', 'company_name', 'description', 'requirements', 'location', 'salary', 'created_at', 'is_active']
        read_only_fields = ['company_name']



#job application
class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    candidate_name = serializers.ReadOnlyField(source='candidate.username')

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_title', 'candidate', 'candidate_name', 'resume', 'cover_letter', 'applied_at', 'status']
        read_only_fields = ['job_title', 'candidate_name', 'applied_at', 'status']




#addin company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'owner', 'website', 'company_size', 'industry']

    # Optional validation to ensure that the owner is an employer
    def validate_owner(self, value):
        if value.role != 'employer':
            raise serializers.ValidationError("Owner must have the role of 'employer'.")
        return value