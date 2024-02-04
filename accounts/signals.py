from .models import Discount
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import threading


@receiver(post_save, sender=Discount)
def send_discount_emails(sender, instance, created, **kwargs):

    if created:
        email_list = User.objects.filter(is_publisher=False).values_list('email', flat=True)

        subject = 'بوکلند: تخفیف جدید!'

        send_email_background_task(subject, 'accounts/discount_email_template.html', instance.code, email_list)


def send_email(subject, from_email, recipient_list, html_content):
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
    )
    for recipient_email in recipient_list:
        email.to = [recipient_email]
        email.attach_alternative(html_content, "text/html")
        email.send()


def send_email_background_task(subject, template, code, recipient_list):
    from_email = "BookLand@email.com"

    context = {'code': code}

    html_content = render_to_string(template, context)

    email_thread = threading.Thread(
        target=send_email,
        args=(subject, from_email, recipient_list, html_content)
    )
    email_thread.start()
