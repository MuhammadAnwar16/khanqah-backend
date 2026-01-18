from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutSectionViewSet, CurrentNasheenViewSet, PreviousNasheenViewSet

router = DefaultRouter()
router.register(r'sections', AboutSectionViewSet, basename='aboutsection')
router.register(r'current-nasheen', CurrentNasheenViewSet, basename='currentnasheen')
router.register(r'previous-nasheen', PreviousNasheenViewSet, basename='previousnasheen')

urlpatterns = [
    path('', include(router.urls)),
]

