from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import threading


def send_email(subject, from_email, recipient_list, html_content):
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_email_background_task(subject, template, code, email):
    from_email = "BookLand@email.com"
    recipient_list = [email]

    context = {'code': code}

    html_content = render_to_string(template, context)

    email_thread = threading.Thread(
        target=send_email,
        args=(subject, from_email, recipient_list, html_content)
    )
    email_thread.start()
