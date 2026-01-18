from django.urls import path
from .views import PublicationList

urlpatterns = [
    path('publications/', PublicationList.as_view(), name='publication-list'),
]
