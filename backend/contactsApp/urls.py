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
)

router = DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"regions", RegionViewSet)
router.register(r"cities", CityViewSet)
router.register(r"branches", BranchViewSet)
router.register(r"contacts", ContactViewSet)
router.register(r"register", RegisterViewSet)

urlpatterns = router.urls
