from django.db import models


class Country(models.Model):
    """
    Modello per rappresentare le Nazioni.
    """
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name'] # Ordina di default per nome

    def __str__(self):
        return f"{self.iso_code} - {self.name}"

class Region(models.Model):
    """
    Modello per rappresentare le Regioni/Stati/Province all'interno di una Nazione.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE, # Se cancello la nazione, cancello le sue regioni
    )
    code = models.CharField(
        max_length=10,
        blank=True, # Potrebbe non essere sempre presente
    )
    name = models.CharField(
        max_length=50
    )

    class Meta:
        ordering = ['name'] # Ordina per nome

    def __str__(self):
        return f"{self.name} ({self.country.iso_code})"

class City(models.Model):
    """
    Modello per rappresentare le Città/Comuni all'interno di una Regione.
    """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE, # Se cancello la regione, cancello le sue città
    )
    name = models.CharField(
        max_length=100 # Aumentato per nomi lunghi
    )
    # Potrebbe essere utile aggiungere il CAP (postal_code) qui se una città
    # ha un solo CAP principale, altrimenti va nel modello Indirizzo.
    # postal_code = models.CharField(_("CAP"), max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['region', 'name'] # Ordina per regione e poi per nome

    def __str__(self):
        return f"{self.name} ({self.region.code})"

# Modelli Anagrafica/Contatti
# ===========================

class Sede(models.Model):
    """
    Modello per rappresentare le Sedi/Filiali di un'organizzazione.
    """
    code = models.CharField(
        max_length=20,
        unique=True,
    )
    name = models.CharField(
        max_length=100
    )
    # Si potrebbero aggiungere qui dettagli della sede come indirizzo, telefono, etc.
    # se rilevanti indipendentemente dai contatti specifici.

    class Meta:
        verbose_name_plural = "Sedi"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=50, verbose_name="Ragione sociale")
    address = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='contacts')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='contacts')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='contacts')
    
    # Campi per l'anagrafica
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name}"
    # Proprietà per accedere facilmente a Regione e Nazione (opzionale ma comodo)
    @property
    def region(self):
        return self.city.region

    @property
    def country(self):
        return self.city.region.country

class Register(models.Model):
    # Campi per l'anagrafica
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"