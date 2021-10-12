from django.urls import path
from rest_framework import routers
from .views import SolvierViewset

router = routers.DefaultRouter()
router.register(r'soldiers', SolvierViewset)

urlpatterns = router.urls