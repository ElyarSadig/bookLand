import threading
from django.core.mail import EmailMessage


def send_email(subject, body, from_email, recipient_list):
    email = EmailMessage(
        subject=subject,
        from_email=from_email,
        body=body,
        to=recipient_list,
    )
    email.send()


def send_email_background_task(activation_code, email):
    subject = "Email Verification"
    body = f"Here is your activation code {activation_code}"
    from_email = "BookLand@email.com"
    recipient_list = [email]

    email_thread = threading.Thread(target=send_email, args=(subject, body, from_email, recipient_list))
    email_thread.start()