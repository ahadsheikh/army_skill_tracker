from django.urls import path
from rest_framework import routers
from .views import ClerkViewSet

from . import views

router = routers.DefaultRouter()
router.register(r'clerks', ClerkViewSet)

urlpatterns = [
    path('create/', views.ClerkCreateView.as_view(), name='create'),
    path('decodejwt/', views.DecodeJWT.as_view(), name='decodejwt'),
]

urlpatterns += router.urls