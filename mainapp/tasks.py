import logging

from celery import shared_task
from django.core.mail import send_mail

from authapp.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_feedback_to_email(message_body: str, message_from: int = None) -> None:
    logger.info(f'Send message: from {message_from}, message:"{message_body}"')
    if message_from is not None:
        user_from = User.objects.filter(pk=message_from).first().get_full_name()
    else:
        user_from = 'Аноним'

    send_mail(
        subject=f'Feedback from {user_from}',
        message=message_body,
        recipient_list=['support@blms.local'],
        from_email='support@blms.local',
        fail_silently=False
    )
