import django_filters   
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
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
        fields = ["region", "region__country"]

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(name__icontains=value) | Q(postcode__startswith=value) )


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_class = CityFilter
    pagination_class = StandardPagination



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
    pagination_class = StandardPagination
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    ordering_fields = ["code", "name"]


class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    filterset_fields = ["code", "name"]
    ordering_fields = ["code", "name"]

search_operations = ["exact", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith"]

class ContactsFilter(django_filters.FilterSet):
    # sede__icontains = django_filters.CharFilter(field_name="sede__name", lookup_expr="icontains")
    # country__icontains = django_filters.CharFilter(field_name="country__name", lookup_expr="icontains")
    # city__icontains = django_filters.CharFilter(field_name="city__name", lookup_expr="icontains")

    class Meta:
        model = Contact
        fields = {
            "register": ["exact"],
            "id": ["exact", "lt", "gt", "lte", "gte", "range"],
            "name": search_operations,
            "email": search_operations,
            "phone": search_operations,
            "phone_ext": search_operations,
            "address": search_operations,
            "country__name": search_operations,
            "country": ["exact"],
        }


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()

    filterset_class = ContactsFilter
    pagination_class = StandardPagination

    # ordering_fields = ["name", "country__name"]
    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return ContactSerializer
        return ContactListSerializer



class RegisterFilter(django_filters.FilterSet):

    class Meta:
        model = Register
        fields = {
            "id": ["exact", "lt", "gt", "lte", "gte", "range"],
            "last_name": search_operations,
            "first_name": search_operations,
            "email": search_operations,
            "phone": search_operations,
            "phone_ext":search_operations,
            "mobile":search_operations,
            "vat_number":search_operations,
        }

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    filterset_class = RegisterFilter
    ordering_fields = ["first_name", "last_name", "phone", "phone_ext", "mobile", "email", "vat_number"]
    pagination_class = StandardPagination

    @action(detail=False, methods=['post'], url_path='check-email')
    def check_email(self, request):
        email = request.data.get('email', '').strip()
        id = request.data.get('id')
        exists = self.queryset.filter(email__iexact=email).exclude(id=id).exists()
        return Response({'available': not exists})