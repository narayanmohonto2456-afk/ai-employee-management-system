from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import email_verification_token

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.html import strip_tags


class EmailService:

#   Handles all email-related functionality.


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
    @staticmethod
    def send_password_reset_email(request, user):
        
        # Send password reset email to the user.

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        current_site = get_current_site(request)

        context = {
            "user": user,
            "domain": current_site.domain,
            "uid": uid,
            "token": token,
            "protocol": "https" if request.is_secure() else "http",
        }

        subject = "Reset Your Password - Enterprise AI HRMS"

        html_message = render_to_string(
            "emails/password_reset.html",
            context,
        )

        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
        )
    