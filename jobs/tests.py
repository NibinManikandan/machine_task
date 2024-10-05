from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Company, JobListing, JobApplication

CustomUser = get_user_model()

class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'role': 'candidate'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_user_login(self):
        # Register a user
        self.test_user_registration()
        
        # Now log in
        login_url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class CompanyTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer = CustomUser.objects.create_user(
            username='employeruser',
            password='employerpassword123',
            email='employer@example.com',
            role='employer'
        )
        self.company_url = reverse('company-create')

    def test_create_company(self):
        self.client.force_authenticate(user=self.employer)
        data = {
            'name': 'Test Company',
            'location': 'New York',
            'description': 'A great company',
            'website': 'https://testcompany.com',
            'company_size': 100,
            'industry': 'Technology'
        }
        response = self.client.post(self.company_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'Test Company')


class JobListingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer = CustomUser.objects.create_user(
            username='employeruser',
            password='employerpassword123',
            email='employer@example.com',
            role='employer'
        )
        self.company = Company.objects.create(
            name='Test Company',
            location='New York',
            description='A great company',
            owner=self.employer
        )
        self.job_list_url = reverse('job-list-create')

    def test_create_job_listing(self):
        self.client.force_authenticate(user=self.employer)
        data = {
            'title': 'Software Engineer',
            'company': self.company.pk,
            'description': 'Develop and maintain software.',
            'requirements': '3+ years of experience.',
            'location': 'Remote',
            'salary': 80000,
            'is_active': True
        }
        response = self.client.post(self.job_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobListing.objects.count(), 1)
        self.assertEqual(JobListing.objects.get().title, 'Software Engineer')

    def test_retrieve_job_listing(self):
        self.test_create_job_listing()
        job_listing = JobListing.objects.get()
        job_detail_url = reverse('job-detail', kwargs={'pk': job_listing.pk})
        
        response = self.client.get(job_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Software Engineer')


class JobApplicationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.candidate = CustomUser.objects.create_user(
            username='candidateuser',
            password='candidatepassword123',
            email='candidate@example.com',
            role='candidate'
        )
        self.employer = CustomUser.objects.create_user(
            username='employeruser',
            password='employerpassword123',
            email='employer@example.com',
            role='employer'
        )
        self.company = Company.objects.create(
            name='Test Company',
            location='New York',
            description='A great company',
            owner=self.employer
        )
        self.job_listing = JobListing.objects.create(
            title='Software Engineer',
            company=self.company,
            description='Develop and maintain software.',
            requirements='3+ years of experience.',
            location='Remote',
            salary=80000
        )
        self.job_application_url = reverse('application-list-create')

    def test_apply_for_job(self):
        self.client.force_authenticate(user=self.candidate)
        data = {
            'job': self.job_listing.pk,
            'resume': 'path/to/resume.pdf',
            'cover_letter': 'I am a great fit for this job.'
        }
        response = self.client.post(self.job_application_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)
        self.assertEqual(JobApplication.objects.get().job.title, 'Software Engineer')


class JobApplicationStatusUpdateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer = CustomUser.objects.create_user(
            username='employeruser',
            password='employerpassword123',
            email='employer@example.com',
            role='employer'
        )
        self.company = Company.objects.create(
            name='Test Company',
            location='New York',
            owner=self.employer
        )
        self.job_listing = JobListing.objects.create(
            title='Software Engineer',
            company=self.company,
            description='Develop and maintain software.',
            requirements='3+ years of experience.',
            location='Remote',
            salary=80000
        )
        self.candidate = CustomUser.objects.create_user(
            username='candidateuser',
            password='candidatepassword123',
            email='candidate@example.com',
            role='candidate'
        )
        self.application = JobApplication.objects.create(
            job=self.job_listing,
            candidate=self.candidate,
            resume='path/to/resume.pdf'
        )
        self.update_status_url = reverse('update-job-application-status', kwargs={'pk': self.application.pk})

    def test_update_application_status(self):
        self.client.force_authenticate(user=self.employer)
        data = {'status': 'accepted'}
        response = self.client.patch(self.update_status_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'accepted')
