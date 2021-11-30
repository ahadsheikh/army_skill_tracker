from django.urls import path
from rest_framework import routers
from .views import (
    SolvierViewset, 
    CriteriaViewset, 
    SubCriteriaViewset, 
    ObservationsViewset,
    CriteriaChangeView,
    MakeCriteria,
    AssessmentView,
    SoldierObservationView
)

router = routers.DefaultRouter()
router.register(r'soldiers', SolvierViewset)
router.register(r'criterias', CriteriaViewset)
router.register(r'subcriterias', SubCriteriaViewset)
router.register(r'observations', ObservationsViewset)


urlpatterns = [
    path('change-criteria/<int:id>/', CriteriaChangeView.as_view(), name='criteria_change'),
    path('make-criterias/', MakeCriteria.as_view(), name='make_criteria'),
    path('assessment/soldier/<int:s_id>/criteria/<int:c_id>/', AssessmentView.as_view(), name='assessment'),
    path('observations/soldier/<int:id>/', SoldierObservationView.as_view(), name='observations')
]

urlpatterns += router.urls