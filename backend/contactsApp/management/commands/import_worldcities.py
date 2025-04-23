import csv, os
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

from contactsApp.models import Country, City, Region

class Command(BaseCommand):
    def handle(self, *args, **options):
        # costrusce il percorso del file
        csv_path = os.path.join(settings.BASE_DIR, "contactsApp/data", "world_cities_geoname.csv")
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {csv_path}"))
            return
        

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            added_countries = set()
            added_regions = set()
            added_cities = 0
        
            with transaction.atomic():
                for row in reader:
                    iso_code = row.get("code")
                    country_name = row.get("country")
                    region_name = row.get("region")
                    province_code = row.get("province")
                    city_name = row.get("name_en")
            
                    country, created = Country.objects.get_or_create(
                        iso_code = iso_code,
                        defaults={'name': country_name}
                    )
                    if created:
                        added_countries.add(country_name)
                    
                    region_key  = (region_name, country.iso_code)
                    if region_key not in added_regions:
                        region, _ = Region.objects.get_or_create(
                            name = region_name,
                            country = country,
                            defaults={'code': province_code}
                        )
                        if not created and not region.code:
                            region.code = province_code
                            region.save()
                        added_regions.add(region_key)
                    else:
                        region = Region.objects.get(name=region_name, country=country)
                        if not region.code:
                            region.code = province_code
                            region.save()

                    city, created = City.objects.get_or_create(
                        name = city_name,
                        region = region
                    )
                    if created:
                        added_cities += 1


        self.stdout.write(self.style.SUCCESS(
            f"Importazione completata: "
            f"{len(added_countries)} nazioni, "
            f"{len(added_regions)} regioni, "
            f"{added_cities} citta' importate. "
        ))       