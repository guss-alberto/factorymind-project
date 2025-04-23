from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
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

    def validate_code(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("il code deve essere integer")
        return value



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
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(read_only=True)
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

    def validate_phone(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("il phone number deve essere integer")
        if not re.match(r'^\+\d+ \d+$', value):
            raise serializers.ValidationError("Il phone number deve iniziare con '+' seguito da uno spazio e numeri")
        return value

    def validate_mobile(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("il mobile field deve essere integer")
        if not re.match(r'^\+\d+ \d+$', value):
            raise serializers.ValidationError("Il mobile number deve iniziare con '+' seguito da uno spazio e numeri")
        return value