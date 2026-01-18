from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet

router = DefaultRouter()
router.register(r'publications', PublicationViewSet)

urlpatterns = router.urls
