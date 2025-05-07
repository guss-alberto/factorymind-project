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
    branch_display = django_filters.CharFilter(method='filter_branch_display')

    class Meta:
        model = Contact
        fields = {
            "register": ["exact"],
            "id": ["exact", "lt", "gt", "lte", "gte", "range"],
            "name": search_operations,
            "email": search_operations,
            "phone": search_operations,
            "phone_ext": search_operations,
            "branch__code": search_operations,
            "branch__name": search_operations,
            "address": search_operations,
            "country__name": search_operations,
            "region__name": search_operations,
            "city__name": search_operations,
        }

    def filter_branch_display(self, queryset, name, value):
        return queryset.filter(
            Q(branch__name__icontains=value) | Q(branch__code__icontains=value)
        ).order_by("branch__name")

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().annotate(
                                        branch__name=F('branch__name'),
                                        branch__code=F('branch__code'),
                                        branch_display=Concat(
                                            F('branch__code'),
                                            Value(' - '),
                                            F('branch__name'),
                                            output_field=CharField()
                                        ),
                                        country__name=F('country__name'),
                                        region__name=F('region__name'),
                                        city__name=F('city__name')
                                    )
    filterset_class = ContactFilter
    ordering_fields = ["name", "email", "phone", "phone_ext", "branch_display"]

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
    serializer_class = DivisionSerializer
    ordering_fields = ["name"]
    filterset_fields = ["register"]