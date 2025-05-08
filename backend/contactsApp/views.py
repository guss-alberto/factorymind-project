import django_filters   
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import F
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import City, Contact, Country, Region, Branch, Register, RegistryType, Division
from .serializer import (
    CitySerializer,
    ContactListSerializer,
    ContactSerializer,
    CountrySerializer,
    RegionSerializer,
    BranchSerializer,
    RegisterSerializer,
    RegistryTypeSerializer,
    DivisionSerializer,
    DivisionListSerializer,
)


class RegionFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Region
        fields = ["country"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(code__icontains=value)
        ).order_by("name")

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_class = RegionFilter
    search_fields = ["name"]
    ordering_fields = ["code", "name"]


class CityFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = City
        fields = ["region", "region__country", "country"]

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(name__icontains=value) | Q(postcode__startswith=value) ).order_by("name")


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_class = CityFilter


class CountryFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Country
        fields = ["iso_code"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(iso_code__icontains=value)
        ).order_by("name")
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_class = CountryFilter
    ordering_fields = ["code", "name"]
    page_size = 100
  

class BranchFilter(django_filters.FilterSet):
    _search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Branch
        fields = ["code"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(code__icontains=value)
        ).order_by("name")

class BranchViewSet(viewsets.ModelViewSet):
    
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filterset_class = BranchFilter
    ordering_fields = ["code", "name"]

class RegistryTypeViewSet(viewsets.ModelViewSet):
    
    queryset = RegistryType.objects.all()
    serializer_class = RegistryTypeSerializer
    ordering_fields = ["name"]
    

search_operations = ["exact", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith"]

class ContactFilter(django_filters.FilterSet):
    branch_display__icontains = django_filters.CharFilter(method='filter_branch_display')
    country_display__icontains = django_filters.CharFilter(method='filter_country_display')
    city_display__icontains = django_filters.CharFilter(method='filter_city_display')
    region_display__icontains = django_filters.CharFilter(method='filter_region_display')

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
            "region__name": search_operations,
            "city__name": search_operations,
        }

    def filter_branch_display(self, queryset, name, value):
        return queryset.filter(branch_display__icontains=value).order_by("branch_display")

    def filter_country_display(self, queryset, name, value):
        return queryset.filter(country_display__icontains=value).order_by("country_display")
    
    def filter_city_display(self, queryset, name, value):
        return queryset.filter(city_display__icontains=value).order_by("city_display")

    def filter_region_display(self, queryset, name, value):
        return queryset.filter(region_display__icontains=value).order_by("region_display")


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().annotate(
                                        branch_display=Concat(
                                            F('branch__code'),
                                            Value(' - '),
                                            F('branch__name'),
                                            output_field=CharField()
                                        ),
                                        country_display=Concat(
                                            F('country__iso_code'),
                                            Value(' - '),
                                            F('country__name'),
                                            output_field=CharField()
                                        ),
                                        city_display=Concat(
                                            F('city__postcode'),
                                            Value(' - '),
                                            F('city__name'),
                                            output_field=CharField()
                                        ),
                                        region_display=Concat(
                                            F('region__code'),
                                            Value(' - '),
                                            F('region__name'),
                                            output_field=CharField()
                                        )
                                    )
    filterset_class = ContactFilter
    filterset_backend = [DjangoFilterBackend]
    # annotated filtered fields
    filter_fields = ['branch_display', 'country_display', 'city_display', 'city__name', 'region_display']
    ordering_fields = ["name", "email", "phone", "phone_ext", "branch_display", "country_display", "region_display"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return ContactSerializer
        return ContactListSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    filterset_fields = {
        "id": ["exact", "lt", "gt", "lte", "gte", "range"],
        "last_name": search_operations,
        "first_name": search_operations,
        "email": search_operations,
        "phone": search_operations,
        "phone_ext":search_operations,
        "mobile":search_operations,
        "vat_number":search_operations,
    }

    @action(detail=False, methods=['post'], url_path='check-email')
    def check_email(self, request):
        email = request.data.get('email', '').strip()
        id = request.data.get('id')
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'email not valid'},
                status=status.HTTP_400_BAD_REQUEST 
            )
        exists = self.queryset.filter(email__iexact=email).exclude(id=id).exists()
        return Response({'available': not exists})


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()   
    ordering_fields = ["name"]
    filterset_fields = ["client", "supplier"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return DivisionSerializer
        return DivisionListSerializer

class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.filter(
            registry_type__name__in=["Fornitore", "Cliente/Fornitore"]  
        ).distinct()
    serializer_class = RegisterSerializer
    