import csv, os
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

from contactsApp.models import Country, City, Region

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Build path for world cities file
        csv_path = os.path.join(settings.BASE_DIR, "contactsApp/data", "world_cities_geoname.csv")
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {csv_path}"))
            return
        
        # Load Italian postal codes into a dictionary
        zipcodes_path = os.path.join(settings.BASE_DIR, "contactsApp/data", "zipcodes.it.csv")
        postcode_map = {}
        
        if os.path.exists(zipcodes_path):
            self.stdout.write(self.style.SUCCESS(f"Loading postal codes from {zipcodes_path}"))
            with open(zipcodes_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    place = row.get("place")
                    province = row.get("province_code")
                    zipcode = row.get("zipcode")
                    
                    if place and zipcode:
                        # Create a compound key with place and province
                        key = f"{place.lower()}"
                        # if province:
                        #     key += f"-{province.lower()}"
                            
                        if key not in postcode_map:
                            postcode_map[key] = zipcode
            
            self.stdout.write(f"Loaded {len(postcode_map)} postal codes")

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            added_countries = set()
            added_regions = set()
            added_cities = 0
            updated_postcodes = 0
        
            with transaction.atomic():
                for row in reader:
                    iso_code = row.get("code")
                    country_name = row.get("country")
                    province = row.get("province")
                    city_name = row.get("name_en")
            
                    country, created = Country.objects.get_or_create(
                        iso_code = iso_code,
                        defaults={'name': country_name}
                    )
                    if created:
                        added_countries.add(country_name)
                    
                    region_key = (province, country.iso_code)
                    if region_key not in added_regions:
                        region, _ = Region.objects.get_or_create(
                            name = province,
                            country = country,
                            defaults={'code': province}
                        )
                        if not region.code:
                            region.code = province
                            region.save()
                        added_regions.add(region_key)
                    else:
                        region = Region.objects.get(name=province, country=country)
                        if not region.code:
                            region.code = province
                            region.save()

                    # For Italian cities, try to find a postal code
                    postcode = None
                    if iso_code == "ITA":
                        # Try different key combinations
                        key = f"{city_name.lower()}"
                        if key in postcode_map:
                            postcode = postcode_map[key]
                        elif province:
                            key_with_province = f"{city_name.lower()}-{province.lower()}"
                            if key_with_province in postcode_map:
                                postcode = postcode_map[key_with_province]

                    city, created = City.objects.get_or_create(
                        name = city_name,
                        region = region,
                        defaults={'postcode': postcode}
                    )
                    
                    # Update existing cities that don't have postcodes
                    if not created and postcode and not city.postcode:
                        city.postcode = postcode
                        city.save()
                        updated_postcodes += 1
                        
                    if created:
                        added_cities += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importazione completata: "
            f"{len(added_countries)} nazioni, "
            f"{len(added_regions)} regioni, "
            f"{added_cities} citta' importate, "
            f"{updated_postcodes} codici postali aggiornati."
        ))