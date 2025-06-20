from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
                    CityViewSet,
                    ContactViewSet,
                    CountryViewSet,
                    RegionViewSet,
                    BranchViewSet,
                    RegisterViewSet,
                    RegistryTypeViewSet,
                    DivisionViewSet,
                    SuppliersViewSet,
                    ClientViewSet,
                    SignViewSet,
                    DepositViewSet,
                    ProfilesAndSubagenciesViewSet
)

router = DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"regions", RegionViewSet)
router.register(r"cities", CityViewSet)
router.register(r"branches", BranchViewSet)
router.register(r"contacts", ContactViewSet)
router.register(r"register", RegisterViewSet, basename="registers")
router.register(r"register_type", RegistryTypeViewSet)
router.register(r"divisions", DivisionViewSet, basename="divisions")
router.register(r"suppliers", SuppliersViewSet, basename="suppliers")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"signes", SignViewSet, basename="signes")
router.register(r"profiles-subagencies", ProfilesAndSubagenciesViewSet, basename="profiles-subagencies")
router.register(r"deposits", DepositViewSet, basename="deposits")


urlpatterns = router.urls
