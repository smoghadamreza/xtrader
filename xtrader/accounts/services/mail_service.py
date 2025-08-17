from typing import List
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class MailService:
    @classmethod
    def mail_users(cls, subject: str, emails: List[str]) -> List[str]:
        failed_emails: List[str] = []

        for email in emails:
            try:
                html_message = render_to_string(
                    "mail_template.html", {"context": "values"}
                )
                plain_message = strip_tags(html_message)

                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception:
                failed_emails.append(email)

        return failed_emails
