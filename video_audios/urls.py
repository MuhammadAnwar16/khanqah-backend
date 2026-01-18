from django.urls import path
from .views import AudioListView, VideoListView

urlpatterns = [
    path("audios/", AudioListView.as_view(), name="audio-list"),
    path("videos/", VideoListView.as_view(), name="video-list"),
]
