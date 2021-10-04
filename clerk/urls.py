from django.urls import path
from rest_framework import routers
from .views import ClerkViewSet

from . import views

router = routers.DefaultRouter()
router.register(r'clerks', ClerkViewSet)

urlpatterns = router.urls