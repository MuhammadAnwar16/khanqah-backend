# contact/urls.py
from django.urls import path
from .views import ContactFormView

urlpatterns = [
    path('send-message/', ContactFormView.as_view(), name='contact_form'),
]
