from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import JobApplication


# Sending email to the candidate when a new job application is submitted
@receiver(post_save, sender=JobApplication)
def send_application_submission_email(sender, instance, created, **kwargs):
    if created:
        candidate_email = instance.candidate.email

        subject = "Thank you for submitting your job application"
        message = f"Dear {instance.candidate.username},\n\n"
        message += f"Thank you for applying for the job: {instance.job.title}.\n"
        message += "Your application has been successfully submitted.\n"
        message += "Our team will review your application and contact you soon.\n\n"
        message += "Best regards,\nCompany Team"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [candidate_email])


# Sendind email to the candidate when the application status is updated by the employer
@receiver(post_save, sender=JobApplication)
def send_application_status_update_email(sender, instance, **kwargs):
    if not instance._state.adding:
        previous_status = instance._history_most_recent().status if hasattr(instance, '_history_most_recent') else None
        if previous_status and previous_status != instance.status:
            candidate_email = instance.candidate.email

            subject = f"Your application status for {instance.job.title} has been updated"
            message = f"Dear {instance.candidate.username},\n\n"
            message += f"Your job application for {instance.job.title} has been updated to '{instance.status}'.\n\n"
            message += "Best regards,\nCompany Team"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [candidate_email])
