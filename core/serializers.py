from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import Criteria, Observation, Soldier, SoldierExtra, SubCriteria, SoldierReport


class SoldierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soldier
        fields = ('id', 'personal_no', 'name', 'rank', 'unit', 
                        'subunit', 'appointment', 'unit_join_date', 'last_promotion_date',
                        'contact', 'date_of_enrollment', 'previous_subunit', 'due_date_of_next_rank')


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
        fields = ('id', 'criteria', 'name', 'subunit', 'mark')


class SubCri(serializers.Serializer):
    id = serializers.IntegerField()
    mark = serializers.IntegerField()


class CriteriaChangeViewSerializer(serializers.Serializer):
    mark = serializers.IntegerField()
    sub_criterias = SubCri(many=True)


class SoldierObservationSeralizer(serializers.Serializer):
    id = serializers.IntegerField()


class ReportFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SoldierReport
        fields = ['evaluation_date_from', 'evaluation_date_to', 'medical_category', 
            'IPFT_first_biannual', 'IPFT_second_biannual', 'RET', 'DIV_order_letter_no_1',
            'DIV_order_letter_no_2', 'DIV_order_letter_no_3', 'fit_for_next_promotion',
            'fit_for_next_promotion_yes_text', 'fit_for_next_promotion_no_text',
            'fit_for_being_instructor', 'fit_for_being_instructor_yes_text',
            'fit_for_being_instructor_no_text', 'fit_for_foreign_mission',
            'fit_for_foreign_mission_yes_text', 'fit_for_foreign_mission_no_text', 
            'recommendation_for_next_appt','special_quality', 'remarks_by_initiating_officer', 'grade']

class SoldierExtraSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SoldierExtra
        fields = ['id', 'soldier', 'medical_category', 'IPFT_first_biannual', 'IPFT_second_biannual', 'RET']



    