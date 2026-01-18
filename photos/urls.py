from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename="collection")
router.register(r'photos', PhotoViewSet, basename="photo")

urlpatterns = [
    path("", include(router.urls)),
]
