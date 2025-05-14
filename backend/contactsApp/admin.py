from django.contrib import admin
from .models import Register, Contact, Country, Region, City, Branch, Division, Sign, Deposit, ProfilesAndSubagencies

admin.site.register(Register)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Branch)
admin.site.register(Division)
admin.site.register(Sign)
admin.site.register(Deposit)
admin.site.register(ProfilesAndSubagencies)