from rest_framework import generics
from .models import Audio, Video
from .serializers import AudioSerializer, VideoSerializer

class AudioListView(generics.ListAPIView):
    queryset = Audio.objects.all().order_by("-date")
    serializer_class = AudioSerializer

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all().order_by("-date")
    serializer_class = VideoSerializer
