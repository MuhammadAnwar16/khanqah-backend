# contact/views.py
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from .serializers import ContactMessageSerializer
from .models import ContactMessage
import logging

logger = logging.getLogger(__name__)


class ContactFormThrottle(AnonRateThrottle):
    """Limit contact form submissions to 10 per hour per IP"""
    rate = '10/hour'


class ContactFormView(APIView):
    """
    Secure contact form endpoint with validation, rate limiting, and database storage.
    Removed @csrf_exempt - now uses proper CSRF protection via DRF.
    """
    throttle_classes = [ContactFormThrottle]
    permission_classes = []  # Public endpoint

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"status": "error", "message": "Validation failed", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save to database
        try:
            contact_message = serializer.save()
        except Exception as e:
            logger.error(f"Error saving contact message: {e}")
            return Response(
                {"status": "error", "message": "Failed to save message"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Send email notification
        try:
            email_subject = f"Contact Form Submission: {contact_message.subject}"
            email_body = f"""
New contact form submission from Khanqah website:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone_number}
Subject: {contact_message.subject}

Message:
{contact_message.message}

---
Submitted at: {contact_message.created_at}
            """

            recipient_email = config('CONTACT_RECIPIENT_EMAIL', default='anwarimdad@gmail.com')
            
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error sending contact email: {e}")
            # Don't fail the request if email fails - message is already saved
            # You can check admin panel for messages even if email fails

        return Response(
            {"status": "success", "message": "Your message has been sent successfully"},
            status=status.HTTP_201_CREATED
        )
