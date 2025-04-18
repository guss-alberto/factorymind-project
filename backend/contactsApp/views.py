from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import City, Contact, Country, Region, Sede
from .serializer import (CitySerializer, ContactListSerializer,
                         ContactSerializer, CountrySerializer,
                         RegionSerializer, SedeSerializer)


class StandardPagination(LimitOffsetPagination):
    page_size = 10
    max_page_size = 100


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_fields = ["code", "name", "country"]
    search_fields = ["name"]
    ordering_fields = ["code", "name"]
    pagination_class = StandardPagination


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ["name", "region"]
    search_fields = ["name"]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ["iso_code", "name"]
    ordering_fields = ["code", "name"]

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    filterset_fields = ["code", "name"]
    ordering_fields = ["code", "name"]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ContactSerializer
        return ContactListSerializer
