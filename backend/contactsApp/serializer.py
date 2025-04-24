from rest_framework import serializers

from .models import City, Contact, Country, Region, Sede, Register


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
        fields = ["id", "name", "region"]
        model = City


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name"]
        model = Sede


class ContactListSerializer(serializers.ModelSerializer):
    sede = serializers.StringRelatedField()
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = [
            "id",
            "sede",
            "name",
            "country",
            "city",
            "region",
            "phone",
            "email",
        ]
        model = Contact


class ContactSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        fields = [
            "id",
            "sede",
            "name",
            "address",
            "country",
            "region",
            "city",
            "first_name",
            "last_name",
            "phone",
            "email",
        ]

        model = Contact


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "first_name", "last_name", "phone", "mobile", "email"]
        model = Register
