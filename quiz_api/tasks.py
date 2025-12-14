from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from .models import DailyReminderSubscriber, EmailLog
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_day1_email(email, streak_count):
    """
    Sends the Day 1 Nurture email with the PDF link.
    Logs the action to the database.
    """
    subject = "🎁 Your Free Gift + Streak Saved!"
    
    # Placeholder for the static file URL
    pdf_url = "https://bible-quiz-mvp.onrender.com/static/guides/psalms_guide.pdf"
    
    context = {
        'app_name': "Bible Quiz App",
        'streak_count': streak_count,
        'pdf_url': pdf_url
    }

    try:
        # 1. Render content
        html_message = render_to_string('emails/day1_nurture.html', context)
        plain_message = strip_tags(html_message)

        # 2. Send Email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        # 3. Log Success
        subscriber = DailyReminderSubscriber.objects.filter(email=email).first()
        if subscriber:
            EmailLog.objects.create(
                subscriber=subscriber,
                email_type='welcome',
                status='sent'
            )
            
        logger.info(f"Sent Day 1 email to {email}")

    except Exception as e:
        logger.error(f"Failed to send Day 1 email to {email}: {str(e)}")
        # Optionally log failure status here


@shared_task
def send_welcome_email(user_email, current_streak):
    """
    Sends a personalized welcome email immediately after subscription.
    Includes a confirmation of the streak and a link to the lead magnet (PDF).
    """
    subject = f"🎁 Your Free Gift + Streak Saved!"
    
    # In a real app, store this file in AWS S3 or Django Static files
    # For MVP, we can point to a placeholder or a static file route
    pdf_download_link = "https://bible-quiz-mvp.onrender.com/static/guides/psalms_guide.pdf"

    # Data to inject into the template
    context = {
        'user_email': user_email,
        'streak_count': current_streak,
        'app_name': "Bible Quiz App",
        'pdf_url': pdf_download_link
    }

    try:
        # Render HTML
        html_message = render_to_string('emails/welcome_email.html', context)
        # Create Plain Text fallback
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Sent welcome email with PDF link to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")

















# old version
# @shared_task
# def send_daily_reminders():
#     """
#     Fetches all active subscribers and sends the daily quiz reminder.
#     """
#     subscribers = DailyReminderSubscriber.objects.filter(is_active=True)
#     count = 0
    
#     logger.info(f"Starting daily reminder task for {subscribers.count()} subscribers.")

#     # Render email content once
#     html_message = render_to_string('emails/daily_reminder.html')
#     plain_message = strip_tags(html_message)
#     subject = "🔥 Keep your streak alive! Daily Bible Quiz"

#     for sub in subscribers:
#         try:
#             send_mail(
#                 subject=subject,
#                 message=plain_message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[sub.email],
#                 html_message=html_message,
#                 fail_silently=False,
#             )
            
#             # Update last sent timestamp
#             sub.last_sent_at = timezone.now()
#             sub.save()
#             count += 1
            
#         except Exception as e:
#             logger.error(f"Failed to send email to {sub.email}: {str(e)}")

#     logger.info(f"Daily reminder task completed. Sent {count} emails.")
#     return f"Sent {count} emails"