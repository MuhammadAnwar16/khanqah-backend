from rest_framework import viewsets
from .models import GalleryCollection
from .serializers import GalleryCollectionSerializer

class GalleryCollectionViewSet(viewsets.ModelViewSet):
    queryset = GalleryCollection.objects.all().prefetch_related('images')
    serializer_class = GalleryCollectionSerializer
