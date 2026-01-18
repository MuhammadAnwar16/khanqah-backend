from rest_framework import viewsets
from .models import Collection, Photo
from .serializers import CollectionSerializer, PhotoSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all().prefetch_related('images').order_by("-created_at")
    serializer_class = CollectionSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
