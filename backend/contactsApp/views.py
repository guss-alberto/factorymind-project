import django_filters
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from .models import City, Contact, Country, Region, Sede, Register
from .serializer import (
    CitySerializer,
    ContactListSerializer,
    ContactSerializer,
    CountrySerializer,
    RegionSerializer,
    SedeSerializer,
    RegisterSerializer,
)


class StandardPagination(LimitOffsetPagination):
    page_size = 10
    max_page_size = 100


class RegionFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Region
        fields = ["country"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(code__icontains=value)
        )

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_class = RegionFilter
    search_fields = ["name"]
    ordering_fields = ["code", "name"]
    pagination_class = StandardPagination


class CityFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = City
        fields = ["region"]

    def filter_search(self, queryset, name, value):
        return queryset.filter( name__icontains=value )


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_class = CityFilter
    search_fields = ["name"]



class CountryFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Country
        fields = ["iso_code"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(iso_code__icontains=value)
        )
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    ordering_fields = ["code", "name"]


class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    filterset_fields = ["code", "name"]
    ordering_fields = ["code", "name"]


class ContactsFilter(django_filters.FilterSet):
    sede__icontains = django_filters.CharFilter(field_name="sede__name", lookup_expr="icontains")
    country__icontains = django_filters.CharFilter(field_name="country__name", lookup_expr="icontains")
    city__icontains = django_filters.CharFilter(field_name="city__name", lookup_expr="icontains")

    class Meta:
        model = Contact
        fields = {
            "id": ["exact", "lt", "gt", "lte", "gte", "range"],
            "name": ["exact", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith"],
            "email": ["exact", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith"],
            "phone": ["exact", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith"],
        }


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()

    filterset_class = ContactsFilter
    pagination_class = StandardPagination

    # ordering_fields = ["name", "country__name"]
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ContactSerializer
        return ContactListSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    filterset_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]