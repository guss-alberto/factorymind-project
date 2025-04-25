from django.db import models


class Country(models.Model):
    """
    Modello per rappresentare le Nazioni.
    """

    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]  # Ordina di default per nome

    def __str__(self):
        return f"{self.iso_code} - {self.name}"


class Region(models.Model):
    """
    Modello per rappresentare le Regioni/Stati/Province all'interno di una Nazione.
    """

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,  # Se cancello la nazione, cancello le sue regioni
    )
    code = models.CharField(
        max_length=10,
        blank=True,  # Potrebbe non essere sempre presente
    )
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]  # Ordina per nome

    def __str__(self):
        return f"{self.name} ({self.country.iso_code})"


class City(models.Model):
    """
    Modello per rappresentare le Città/Comuni all'interno di una Regione.
    """

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["region", "name"]  # Ordina per regione e poi per nome

    def __str__(self):
        return f"{self.name} ({self.postcode})"


# Modelli Anagrafica/Contatti
# ===========================


class Sede(models.Model):
    """
    Modello per rappresentare le Sedi/Filiali di un'organizzazione.
    """

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sedi"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Register(models.Model):
    # Campi per l'anagrafica
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    phone_ext = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    vat_number = models.CharField(max_length=20, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='contacts')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Ragione sociale")
    phone = models.CharField(max_length=20, null=True)
    phone_ext = models.CharField(max_length=20, null=True)
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
