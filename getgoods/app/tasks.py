from django.core.mail import send_mail
from django.conf import settings
from getgoods.celery import celery_app


@celery_app.task
def send_mail_task(recipients, subject, context):
    print(1)
    send_mail(
        subject=subject,
        message=context,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False
    )
    print(2)