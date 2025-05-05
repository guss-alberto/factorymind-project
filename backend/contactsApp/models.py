from django.db import models


class Country(models.Model):
    """
    Models to represent Nations
    """

    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.iso_code} - {self.name}"


class Region(models.Model):
    """
    Model to represent Regions/States/Provinces within a Nation
    """

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country.iso_code})"


class City(models.Model):
    """
    Model to represent Cities within a Region
    """

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ["region", "name"]

    def __str__(self):
        return f"{self.name} ({self.postcode})"


# Models for Personal/Contact Information
# ===========================

class Branch(models.Model):
    """
    Model to represent Offices/Branches of an organization
    """

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Register(models.Model):
    # Campi per l'anagrafica
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    phone_ext = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    vat_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    register = models.ForeignKey(
        Register, on_delete=models.CASCADE, related_name="contacts"
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Ragione sociale")
    phone = models.CharField(max_length=20)
    phone_ext = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
