import csv
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

from contactsApp.models import Country, City, Region


class Command(BaseCommand):
    def handle(self, *args, **options):
        # path creation
        base_path = Path(settings.BASE_DIR) / "contactsApp/data"

        with transaction.atomic():
            with (base_path / "worldcities.csv").open("r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    iso_code = row.get("code")

                    # Skip italy, we'll add it manually later
                    if iso_code == "ITA":
                        continue

                    country_name = row.get("country")
                    province = row.get("province")
                    city_name = row.get("name_en")

                    country, _ = Country.objects.get_or_create(
                        iso_code=iso_code,
                        name=country_name,
                    )
                    
                    region = None
                    if province:
                        region, _ = Region.objects.get_or_create(
                            name=province,
                            country=country,
                        )

                        City.objects.get_or_create(
                            name=city_name,
                            region=region,
                            country=country
                        )

                    else:
                        City.objects.get_or_create(
                            name=city_name,
                            country=country
                        )
                    
                country, _ = Country.objects.get_or_create(
                    iso_code="ITA",
                    name="Italy",
                )

            with (base_path / "zipcodes.it.csv").open("r") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    province_code = row.get("province_code")
                    province_name = row.get("province")

                    city_name = row.get("place")
                    postcode = row.get("zipcode")

                    region, _ = Region.objects.get_or_create(
                        name=province_name,
                        country=country,
                        code=province_code,
                    )

                    City.objects.get_or_create(
                        name=city_name,
                        region=region,
                        postcode=postcode,
                        country=country,
                    )
                    
