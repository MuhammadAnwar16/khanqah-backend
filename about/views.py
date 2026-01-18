from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AboutSection, CurrentNasheen, PreviousNasheen
from .serializers import AboutSectionSerializer, CurrentNasheenSerializer, PreviousNasheenSerializer


class AboutSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get all active About sections with their subsections
    """
    queryset = AboutSection.objects.filter(is_active=True).prefetch_related('subsections')
    serializer_class = AboutSectionSerializer
    
    def get_queryset(self):
        # Return all active sections, ordered by order field
        return AboutSection.objects.filter(is_active=True).prefetch_related(
            'subsections'
        ).order_by('order', 'id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CurrentNasheenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get current active Nasheen
    """
    queryset = CurrentNasheen.objects.filter(is_active=True)
    serializer_class = CurrentNasheenSerializer
    
    def get_queryset(self):
        # Return only the active current Nasheen
        return CurrentNasheen.objects.filter(is_active=True)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        current_nasheen = queryset.first()
        if current_nasheen:
            serializer = self.get_serializer(current_nasheen, context={'request': request})
            return Response(serializer.data)
        return Response(None)


class PreviousNasheenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get all previous Nasheens for lineage tree
    """
    queryset = PreviousNasheen.objects.filter(is_active=True)
    serializer_class = PreviousNasheenSerializer
    
    def get_queryset(self):
        # Return all active previous Nasheens, ordered by order field
        return PreviousNasheen.objects.filter(is_active=True).order_by('order', 'id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

