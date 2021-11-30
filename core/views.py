import json
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError

from clerk.serializers import ImageUploadSerializer
from core.serializers import CriteriaChangeViewSerializer, ObservationSerializer, SoldierSerializer, CriteriaSerializer, SubCriteriaSerializer
from core.models import Criteria, Observation, Soldier, SoldierMark, SubCriteria

    

@api_view(('GET',))
def user_type(requst, id):
    user = get_object_or_404(User, id=id)
    if user.is_superuser:
        return Response({'related_id': -1, 'type': 'admin'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'clerk'):
        return Response({'related_id': user.clerk.id, 'type': 'clerk'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'officer'):
        return Response({'related_id': user.officer.id, 'type': 'officer'}, status=status.HTTP_200_OK)
    else:
        return Response({'related_id': 0, 'type': 'unknown'}, status=status.HTTP_200_OK)



class ProfilePicUpload(generics.GenericAPIView):
    serializer_class = ImageUploadSerializer
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['image']
        user = get_object_or_404(User, pk=id)

        if hasattr(user, 'clerk'):
            clerk = user.clerk
            clerk.image = file
            clerk.profile_pic.save(file.name, file, save=True)
            return Response(status=status.HTTP_200_OK)
        elif hasattr(user, 'officer'):
            officer = user.officer
            officer.image = file
            officer.profile_pic.save(file.name, file, save=True)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "User not a clerk nor a officer"}, status=status.HTTP_404_NOT_FOUND)



class IsAdmin(generics.GenericAPIView):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)

        res = {}
        res['is_admin'] = user.is_superuser

        return Response(res, status=status.HTTP_200_OK)

class SolvierViewset(viewsets.ModelViewSet):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer

    def get_queryset(self):
        q = self.parse_valid_query_params()
        if self.action == 'list':
            if bool(q):
                try:
                    queryset = Soldier.objects.filter(**q)
                except ValidationError as v:
                    queryset = Soldier.objects.none()
                return queryset
            else:
                return Soldier.objects.all()         
        else:
            return Soldier.objects.all()

    def parse_valid_query_params(self):
        q = self.request.query_params
        valid_query_params = ['personal_no', 'name', 'rank', 'address', 'unit',
                        'subunit', 'appointment', 'join_date', 'commision_date', 
                        'previous_company', 'mission']
        q_dict = {}
        for key in q.keys():
            if key in valid_query_params:
                q_dict[key] = q[key]

        return q_dict


class ObservationsViewset(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class CriteriaViewset(viewsets.ModelViewSet):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer


class SubCriteriaViewset(viewsets.ModelViewSet):
    queryset = SubCriteria.objects.all()
    serializer_class = SubCriteriaSerializer


class MakeCriteria(views.APIView):
    def get(self, request):
        base_dir = settings.BASE_DIR
        with open(f'{base_dir}/criterias.json', 'r') as f:
            criterias = json.load(f)
            for c in criterias:
                n = Criteria.objects.filter(name=c['name']).count()
                if n == 0:
                    Criteria.objects.create(name=c['name'])
        
        return Response(status=status.HTTP_200_OK)


class CriteriaChangeView(views.APIView):
    def get(self, request, id):
        criteria = get_object_or_404(Criteria, pk=id)
        c_data = CriteriaSerializer(criteria).data
        c_data['id'] = criteria.id
        c_data['sub_criterias'] = []

        sub_cries = SubCriteria.objects.filter(criteria_id=id)
        for sub_cri in sub_cries:
            s_data = SubCriteriaSerializer(sub_cri).data
            del s_data['criteria']
            s_data['id'] = sub_cri.id
            c_data['sub_criterias'].append(s_data)

        return Response(c_data, status=status.HTTP_200_OK)


    def post(self, request, id):
        cri_change_seri = CriteriaChangeViewSerializer(data=request.data)
        cri_change_seri.is_valid(raise_exception=True)

        criteria = get_object_or_404(Criteria, pk=id)
        criteria.mark = cri_change_seri.validated_data['mark']
        criteria.save()

        for sub_cri in cri_change_seri.validated_data['sub_criterias']:
            sub_criteria = get_object_or_404(SubCriteria, pk=sub_cri['id'])
            sub_criteria.mark = sub_cri['mark']
            sub_criteria.save()

        res = {
            'message': 'Criteria updated successfully'
        }

        return Response(res, status=status.HTTP_200_OK)


class AssessmentView(views.APIView):
    def get(self, request, s_id, c_id):
        soldier = get_object_or_404(Soldier, pk=s_id)
        criteria = get_object_or_404(Criteria, pk=c_id)
        c_data = CriteriaSerializer(criteria).data
        c_data['id'] = criteria.id
        c_data['sub_criterias'] = []

        sum = 0

        sub_cries = SubCriteria.objects.filter(criteria=criteria)
        for sub_cri in sub_cries:
            s_data = SubCriteriaSerializer(sub_cri).data
            del s_data['criteria']
            s_data['id'] = sub_cri.id

            s_mark = SoldierMark.objects.filter(soldier=soldier, sub_criteria=sub_cri).first()
            if s_mark:
                s_data['mark'] = s_mark.mark
                sum += s_mark.mark
            else:
                s_data['mark'] = 0
            c_data['sub_criterias'].append(s_data)
        c_data['mark'] = sum

        return Response(c_data, status=status.HTTP_200_OK)


    def post(self, request, s_id, c_id):    
        cri_change_seri = CriteriaChangeViewSerializer(data=request.data)
        cri_change_seri.is_valid(raise_exception=True)
        
        soldier = get_object_or_404(Soldier, pk=s_id)

        for sub_cri in cri_change_seri.validated_data['sub_criterias']:
            sub_criteria = get_object_or_404(SubCriteria, pk=sub_cri['id'])
            sm = SoldierMark.objects.filter(soldier=soldier, sub_criteria=sub_criteria)
            if sm.count() == 0:
                SoldierMark.objects.create(soldier=soldier, sub_criteria=sub_criteria, mark=sub_cri['mark'])
            else:
                sm.update(mark=sub_cri['mark'])

        res = {
            'message': 'Mark Saved successfully'
        }

        return Response(res, status=status.HTTP_200_OK)