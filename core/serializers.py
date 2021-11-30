from rest_framework import serializers
from .models import Criteria, Observation, Soldier, SubCriteria


class SoldierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soldier
        fields = ('personal_no', 'name', 'rank', 'address', 'unit', 
                        'subunit', 'appointment', 'join_date', 'commision_date',
                        'contact', 'previous_company', 'mission')


class ObservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Observation
        fields = ('id', 'message',)

class CriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = ('id', 'name', 'mark')

class SubCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCriteria
        fields = ('id', 'criteria', 'name', 'mark')


class SubCri(serializers.Serializer):
    id = serializers.IntegerField()
    mark = serializers.IntegerField()


class CriteriaChangeViewSerializer(serializers.Serializer):
    mark = serializers.IntegerField()
    sub_criterias = SubCri(many=True)


class SoldierObservationSeralizer(serializers.Serializer):
    id = serializers.IntegerField()



    