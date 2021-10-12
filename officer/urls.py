from django.urls import path
from rest_framework import routers
from .views import OfficerViewSet

from . import views

router = routers.DefaultRouter()
router.register(r'officers', OfficerViewSet)

urlpatterns = router.urls