from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_task_assignment_email(task_id, assigned_user_email):
    send_mail(
        subject='New Task Assigned',
        message=f'You have been assigned to task ID {task_id}',
        from_email='no-reply@projectmanager.com',
        recipient_list=[assigned_user_email],
        fail_silently=False,
    )

@shared_task
def send_daily_summary_email():
    users = User.objects.all()
    for user in users:
        send_mail(
            subject="Daily Summary",
            message="Here is your daily summary of tasks.",
            from_email="noreply@projectmanager.com",
            recipient_list=[user.email],
        )