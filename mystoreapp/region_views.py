from rest_framework import generics
from .models import City, District
from .serializers import CitySerializer, DistrictSerializer

class CityListCreateAPIView(generics.ListAPIView):
    queryset = City.objects.prefetch_related('district_set')
    serializer_class = CitySerializer

    def perform_create(self, serializer):
        serializer.save()

class DistrictsByCityAPIView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')
        return District.objects.filter(city_id=city_id)