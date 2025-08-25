from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(to_email):
    subject = 'Welcome to JobBoardAPI'
    message = 'Thank you for registering at JobBoardAPI. We are excited to have you on board!'
    from_email = 'cyotero26@gmail.com'
    recipient_list = [to_email]
    send_mail(subject, message, from_email, recipient_list)

    return f'Email sent successfully!'

@shared_task
def send_application_confirmation_email(user_email, job_title, company_name):
    subject = f"Application Received for {job_title}"
    message = (
        f"Dear Candidate,\n\n"
        f"Thank you for applying for the position of {job_title} at {company_name}.\n"
        f"Your application is under review, and the company will get back to you shortly.\n\n"
        f"Best regards,\n"
        f"{company_name} Recruitment Team"
    )
    send_mail (
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=True,
    )