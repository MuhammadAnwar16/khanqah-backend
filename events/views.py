from rest_framework import viewsets
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get all active events
    Read-only viewset for public access
    """
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    
    def get_queryset(self):
        """Return all active events, ordered by order field"""
        return Event.objects.filter(is_active=True).order_by('order', 'id')
    
    def list(self, request, *args, **kwargs):
        """Return list of all active events"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
