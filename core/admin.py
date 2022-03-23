from django.contrib import admin
from .models import *

admin.site.register(Soldier)
admin.site.register(Criteria)
admin.site.register(SubCriteria)
admin.site.register(Observation)
admin.site.register(SoldierReport)
admin.site.register(SoldierMark)
admin.site.register(SoldierExtra)

