from django.urls import path
from rest_framework import routers, views
from .views import (
    SoldierExtraView,
    SolvierViewset, 
    CriteriaViewset, 
    SubCriteriaViewset, 
    ObservationsViewset,
    CriteriaChangeView,
    MakeCriteria,
    AssessmentView,
    SoldierObservationView,
    report_page,
    report_download,
    ReportForm,
    isReportFenerated,
    SoldierExtraBySoldier,
)
from . import views

router = routers.DefaultRouter()
router.register(r'soldiers', SolvierViewset)
router.register(r'criterias', CriteriaViewset)
router.register(r'subcriterias', SubCriteriaViewset)
router.register(r'observations', ObservationsViewset)
router.register(r'soldierextra', SoldierExtraView)


urlpatterns = [
    path('change-criteria/<int:id>/', CriteriaChangeView.as_view(), name='criteria_change'),
    path('make-criterias/', MakeCriteria.as_view(), name='make_criteria'),
    path('assessment/soldier/<int:s_id>/criteria/<int:c_id>/', AssessmentView.as_view(), name='assessment'),
    path('observations/soldier/<int:id>/', SoldierObservationView.as_view(), name='observations'),
    path('test/', report_page, name='report_page'),
    path('report/soldier/<int:id>/', ReportForm.as_view(), name='report_form'),
    path('report/download/check/<int:id>/', isReportFenerated.as_view(), name='is_report_generated'),
    path('report/download/officer/<int:off_id>/soldier/<int:sol_id>/', report_download, name='report_download'),
    path('soldier-extra/soldier/<int:id>/', SoldierExtraBySoldier.as_view(), name='soldier_extra'),
    path('predict/<str:pk/>', views.predict, name='predict')
]

urlpatterns += router.urls