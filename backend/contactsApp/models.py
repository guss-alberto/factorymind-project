from django.db import models


class NameCodeEntity(models.Model):
    """
    Abstract model for entities with a name and optional code
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

class Country(NameCodeEntity):
    """
    Models to represent Nations
    """

    iso_code = models.CharField(max_length=3, unique=True)

    class Meta(NameCodeEntity.Meta):
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.iso_code} - {self.name}"


class Region(NameCodeEntity):
    """
    Model to represent Regions/States/Provinces within a Nation
    """

    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.country.iso_code})"


class City(models.Model):
    """
    Model to represent Cities within a Region
    """

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta: 
        ordering = ["name", "postcode", "region", "country"]

    def __str__(self):
        return f"{self.name} ({self.postcode})"


# Models for Personal/Contact Information
# ===========================

class Branch(NameCodeEntity):
    """
    Model to represent Offices/Branches of an organization
    """

    def __str__(self):
        return f"{self.name}"
    
class RegistryType(NameCodeEntity):
    """
    Model to represent Offices/Branches of an organization
    """

    def __str__(self):
        return f"{self.name}"


class Register(models.Model):
    # Fields for Registry
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    phone_ext = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    registry_type = models.ForeignKey(RegistryType, on_delete=models.CASCADE )

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
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


# Models for Tabs
# ===========================

class Division(NameCodeEntity):
    client = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="client_division",
            limit_choices_to={  #AGGIUNTO QUESTO
            "registry_type__name__in": ["Cliente", "Cliente/Fornitore"]
        }
    )
    supplier = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="supplier_division",
        limit_choices_to={
            "registry_type__name__in": ["Fornitore", "Cliente/Fornitore"]
        }
      )
    def __str__(self):
        return f"{self.code} - {self.name}"

class Sign(NameCodeEntity):
    supplier = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="supplier_signes",
        limit_choices_to={
            "registry_type__name__in": ["Fornitore", "Cliente/Fornitore"]
        }
      )    
    
    def __str__(self):
        return f"{self.name} {self.code}"

class Profiles(models.Model):
    client = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="client_profiles",
        limit_choices_to={ 
            "registry_type__name__in": ["Cliente", "Cliente/Fornitore"]
        }
    )
    supplier = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="supplier_profiles",
        limit_choices_to={
            "registry_type__name__in": ["Fornitore", "Cliente/Fornitore"]
        }
    )
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    sign = models.ForeignKey(Sign, on_delete=models.CASCADE )
    corresponding_code = models.CharField(max_length=50)

class Deposit(NameCodeEntity):
    def __str__(self):
        return f"{self.name} {self.code}"


class Subagengies(models.Model):
    client = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="client_subagencies",
        limit_choices_to={ 
            "registry_type__name__in": ["Cliente", "Cliente/Fornitore"]
        }
    )
    supplier = models.ForeignKey(
        Register, 
        on_delete=models.CASCADE, 
        related_name="supplier_subagencies",
        limit_choices_to={
            "registry_type__name__in": ["Fornitore", "Cliente/Fornitore"]
        }
    )
    sign = models.ForeignKey(Sign, on_delete=models.CASCADE)
    corresponding_code = models.CharField(max_length=50)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)