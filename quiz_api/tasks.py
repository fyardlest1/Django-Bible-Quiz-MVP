from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from .models import DailyReminderSubscriber
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_daily_reminders():
    """
    Fetches all active subscribers and sends the daily quiz reminder.
    """
    subscribers = DailyReminderSubscriber.objects.filter(is_active=True)
    count = 0
    
    logger.info(f"Starting daily reminder task for {subscribers.count()} subscribers.")

    # Render email content once
    html_message = render_to_string('emails/daily_reminder.html')
    plain_message = strip_tags(html_message)
    subject = "🔥 Keep your streak alive! Daily Bible Quiz"

    for sub in subscribers:
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Update last sent timestamp
            sub.last_sent_at = timezone.now()
            sub.save()
            count += 1
            
        except Exception as e:
            logger.error(f"Failed to send email to {sub.email}: {str(e)}")

    logger.info(f"Daily reminder task completed. Sent {count} emails.")
    return f"Sent {count} emails"
