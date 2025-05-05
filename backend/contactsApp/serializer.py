from rest_framework import serializers

from .models import City, Contact, Country, Region, Register, Branch


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["iso_code", "name"]
        model = Country


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name", "country"]
        model = Region


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "region", "postcode"]
        model = City


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name"]
        model = Branch


# visualizzare
class ContactListSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = [
            "id",
            "branch",
            "register",
            "name",
			"phone",
			"phone_ext",
			"email",
            "country",
            "region",
            "city",
			"address",
        ]
        model = Contact


# inserimento
class ContactSerializer(serializers.ModelSerializer):
    register = serializers.PrimaryKeyRelatedField(queryset=Register.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
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

        model = Contact


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "first_name", "last_name", "phone", "phone_ext", "mobile", "email", "vat_number"]
        model = Register
