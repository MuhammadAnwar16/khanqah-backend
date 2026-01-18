from rest_framework.routers import DefaultRouter
from .views import GalleryCollectionViewSet

router = DefaultRouter()
router.register(r'gallery', GalleryCollectionViewSet, basename='gallery')

urlpatterns = router.urls
