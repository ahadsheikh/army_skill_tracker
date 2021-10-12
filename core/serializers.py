from rest_framework import serializers
from .models import Soldier


class SoldierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soldier
        fields = ('personal_no', 'name', 'rank', 'address', 'unit', 
                        'subunit', 'appointment', 'join_date', 'commision_date',
                        'contact', 'previous_company', 'mission')