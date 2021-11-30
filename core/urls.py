from django.urls import path
from rest_framework import routers
from .views import (
    SolvierViewset, 
    CriteriaViewset, 
    SubCriteriaViewset, 
    ObservationsViewset,
    CriteriaChangeView,
    MakeCriteria
)

router = routers.DefaultRouter()
router.register(r'soldiers', SolvierViewset)
router.register(r'criterias', CriteriaViewset)
router.register(r'subcriterias', SubCriteriaViewset)
router.register(r'observations', ObservationsViewset)


urlpatterns = [
    path('change-criteria/<int:id>/', CriteriaChangeView.as_view(), name='criteria_change'),
    path('make-criterias/', MakeCriteria.as_view(), name='make_criteria'),
]

urlpatterns += router.urls