from rest_framework import serializers

from .models import City, Contact, Country, Region, Register, Branch, RegistryType, Division


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "iso_code", "name"]
        model = Country


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name", "country"]
        model = Region


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "region", "postcode", "country"]
        model = City


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name"]
        model = Branch


# visualizzare
class ContactListSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(read_only=True)
    branch__name = serializers.CharField(read_only=True)
    branch__code = serializers.CharField(read_only=True)
    branch_display = serializers.CharField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    country__name = serializers.CharField(read_only=True)
    country__iso_code = serializers.CharField(read_only=True)
    country_display = serializers.CharField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    city__name = serializers.CharField(read_only=True)
    city__postcode = serializers.CharField(read_only=True)
    city_display = serializers.CharField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(read_only=True)
    region__name = serializers.CharField(read_only=True)
    region__code = serializers.CharField(read_only=True)
    region_display = serializers.CharField(read_only=True)

    class Meta:
        fields = [
            "id",
            "branch",
            "branch__name",
            "branch__code",
            "branch_display",
            "register",
            "name",
			"phone",
			"phone_ext",
			"email",
            "country",
            "country__name",
            "country__iso_code",
            "country_display",
            "region",
            "region__name",
            "region__code",
            "region_display",
            "city",
            "city__name",
            "city__postcode",
            "city_display",
			"address",
        ]
        model = Contact


# inserimento
class ContactSerializer(serializers.ModelSerializer):
    register = serializers.PrimaryKeyRelatedField(queryset=Register.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), allow_null=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Contact
        fields = [
            "id",
            "register",
            "branch",
            "name",
            "phone",
            "phone_ext",
            "email",
            "country",
            "region",
            "city",
            "address",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    registry_type_display = serializers.CharField(read_only=True)
    registry_type__name = serializers.CharField(read_only=True)

    class Meta:
        fields = ["id", "first_name", "last_name", "phone", "phone_ext", "mobile", "email", "vat_number", "registry_type", "registry_type_display", "registry_type__name"]
        model = Register

  
class RegistryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = RegistryType

#inserimento
class DivisionSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Register.objects.all())

    class Meta:
        fields = ["id", "name", "code", "client", "supplier"]
        model = Division

#visualizzare
class DivisionListSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)
    supplier__name = serializers.CharField(read_only=True)
    supplier__last_name = serializers.CharField(read_only=True)
    supplier_display = serializers.CharField(read_only=True)

    class Meta:
        fields = ["id", "name", "code", "client", "supplier", "supplier__name", "supplier__last_name", "supplier_display"]
        model = Division


