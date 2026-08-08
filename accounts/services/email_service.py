from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import email_verification_token


class EmailService:
    """
    Handles all email-related functionality.
    """

    @staticmethod
    def send_verification_email(request, user):

        current_site = get_current_site(request)

        context = {
            "user": user,
            "domain": current_site.domain,
            "protocol": "https" if request.is_secure() else "http",
            "uid": urlsafe_base64_encode(
                force_bytes(user.pk)
            ),
            "token": email_verification_token.make_token(user),
        }

        html_message = render_to_string(
            "emails/verify_email.html",
            context,
        )

        email = EmailMultiAlternatives(
            subject="Verify Your Email Address",
            body="Please verify your email.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send()