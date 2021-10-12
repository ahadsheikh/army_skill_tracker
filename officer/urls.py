from django.urls import path
from rest_framework import routers
from .views import OfficerViewSet


router = routers.DefaultRouter()
router.register(r'officers', OfficerViewSet)

urlpatterns = router.urls