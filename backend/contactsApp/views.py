import django_filters   
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import City, Contact, Country, Region, Branch, Register, RegistryType, Division, Sign, Profiles,Deposit, Subagengies
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
    SignSerializer,
    ProfilesSerializer,
    ProfilesListSerializer,
    DepositSerializer,
    SubagenciesSerializer,
    SubagenciesListSerializer,
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
                                        branch_display=Concat(      #annotations for display
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
    
class RegisterFilter(django_filters.FilterSet):
    registry_type_display__icontains = django_filters.CharFilter(method='filter_registry_type_display')

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

    def filter_registry_type_display(self, queryset, name, value):
        return queryset.filter(registry_type_display__icontains=value).order_by("last_name")
    

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all().annotate(
        registry_type_display = F('registry_type__name')  # annotation for display
    )   
    serializer_class = RegisterSerializer
    filterset_class = RegisterFilter
    ordering_fields = ["last_name", "first_name", "email", "phone", "phone_ext", "mobile", "vat_number", "registry_type_display"]

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

class DivisionFilter(django_filters.FilterSet):
    supplier_display__icontains = django_filters.CharFilter(method='filter_supplier_display')
   
    class Meta:
        model = Division
        fields = {"client", "supplier"}

    def filter_supplier_display(self, queryset, name, value):
        return queryset.filter(supplier_display__icontains=value).order_by("supplier_display", "name")

class DivisionViewSet(viewsets.ModelViewSet):
    filterset_class = DivisionFilter
    filter_fields = ["supplier_display"]
    ordering_fields = ["name", "supplier_display"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return DivisionSerializer
        return DivisionListSerializer

    def get_queryset(self):
        queryset = Division.objects.all().annotate(
            supplier_display = Concat(
                F('supplier__last_name'),
                Value(' - '),
                F('supplier__first_name'),
                output_field=CharField()  # annotation for display
            )
        )

        excluded_supplier = self.request.query_params.get("excluded_supplier")
        if excluded_supplier and excluded_supplier.isdigit():
            queryset = queryset.exclude(supplier=int(excluded_supplier))

        return queryset.distinct()

class SuppliersViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = Register.objects.filter(
            registry_type__name__in=["Fornitore", "Cliente/Fornitore"]
        )

        excluded_id = self.request.query_params.get("excluded_id")
        if excluded_id and excluded_id.isdigit():
            queryset = queryset.exclude(id=int(excluded_id))

        return queryset.distinct()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.filter(
            registry_type__name__in=["Cliente", "Cliente/Fornitore"]  
        ).distinct()
    serializer_class = RegisterSerializer
    
class SignViewSet(viewsets.ModelViewSet):
    serializer_class = SignSerializer

    def get_queryset(self):
        queryset = Sign.objects.all()

        excluded_supplier = self.request.query_params.get("excluded_supplier")
        if excluded_supplier and excluded_supplier.isdigit():
            queryset = queryset.exclude(supplier=int(excluded_supplier))

        return queryset.distinct()


class ProfileFilter(django_filters.FilterSet):
    supplier_display__icontains = django_filters.CharFilter(method='filter_supplier_display')
    division_display__icontains = django_filters.CharFilter(method='filter_division_display')
    sign_display__icontains = django_filters.CharFilter(method='filter_sign_display')

    class Meta:
        model = Profiles
        fields = {
                "corresponding_code": search_operations,
                "client": ["exact"],
                }

    def filter_supplier_display(self, queryset, name, value):
        return queryset.filter(supplier_display__icontains=value).order_by("supplier_display")

    def filter_division_display(self, queryset, name, value):
        return queryset.filter(division_display__icontains=value).order_by("division_display")

    def filter_sign_display(self, queryset, name, value):
        return queryset.filter(sign_display__icontains=value).order_by("sign_display")


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profiles.objects.all().annotate(
        supplier_display = Concat(
            F('supplier__last_name'), 
            Value(' - '),
            F('supplier__first_name'),
            output_field=CharField()
        ),
        division_display = Concat(
            F('division__code'), 
            Value(' - '),
            F('division__name'),
            output_field=CharField()
        ),
        sign_display = Concat(
            F('sign__code'), 
            Value(' - '),
            F('sign__name'),
            output_field=CharField()
        )
    )
    filterset_class = ProfileFilter
    filter_fields = ["supplier_display", "division_display", "sign_display", "corresponding_code"]
    ordering_fields = [ "supplier_display", "division_display", "sign_display", "corresponding_code"]
   

    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return ProfilesSerializer
        return ProfilesListSerializer

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


class SubagenciesFilter(django_filters.FilterSet):
    client_display__icontains = django_filters.CharFilter(method='filter_client_display')

    class Meta:
        model = Subagengies
        fields = {"client"}

    def filter_client_display(self, queryset, name, value):
        return queryset.filter(client_display__icontains=value).order_by("client_display", "name")


class SubagenciesViewSet(viewsets.ModelViewSet):
    queryset = Subagengies.objects.all().annotate(
        client_display = Concat(
            F('client__last_name'), 
            Value(' - '),
            F('client__first_name'),
            output_field=CharField()
        )
    )
    filterset_class = SubagenciesFilter
    filter_fields = ["client_display"]
    ordering_fields = ["client_display" ]
   

    def get_serializer_class(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            return SubagenciesSerializer
        return SubagenciesListSerializer