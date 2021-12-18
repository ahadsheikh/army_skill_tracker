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

from django.template.loader import get_template
from django.http import HttpResponse
import weasyprint

from clerk.serializers import ImageUploadSerializer
from core.serializers import ( CriteriaChangeViewSerializer, ObservationSerializer, 
                                SoldierObservationSeralizer, SoldierSerializer, 
                                CriteriaSerializer, SubCriteriaSerializer, ReportFormSerializer )
from core.models import Criteria, Observation, Soldier, SoldierMark, SubCriteria, SoldierReport
from officer.models import Officer
    

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


class SoldierObservationView(views.APIView):
    def get(self, request, id):
        soldier = get_object_or_404(Soldier, pk=id)
        observations = soldier.observations.all()
        data = []
        for observation in observations:
            o_data = ObservationSerializer(observation).data
            data.append(o_data)
        
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, id):
        observation_seri = SoldierObservationSeralizer(data=request.data, many=True)
        observation_seri.is_valid(raise_exception=True)

        soldier = get_object_or_404(Soldier, pk=id)

        data = {
            "message": "Added Successfully",
            "failed": []
        }
        soldier.observations.clear()
        for observation in observation_seri.validated_data:
            try:
                ob = Observation.objects.get(id=observation['id'])
                soldier.observations.add(ob)

            except Observation.DoesNotExist:
                data['failed'].append(observation)
            

        return Response(data, status=status.HTTP_200_OK)


class ReportForm(views.APIView):

    # Make a one word string to capitalize multi word string
    def string_capitalize(self, str):
        l = len(str)
        i = 0
        while i < l:
            if i == 0:
                str = str[0].upper() + str[1:]
            elif str[i] == '_':
                str = str[:i] + ' ' + str[i+1].upper() + str[i+2:]
                i += 1
            i += 1
        return str

    def get(self, request, id):
        soldier = get_object_or_404(Soldier, pk=id)
        marks = SoldierMark.objects.filter(soldier=soldier)
        cri = {}
        total = 0
        for mark in marks:
            if mark.sub_criteria.criteria.name not in cri:
                cri[mark.sub_criteria.criteria.name] = int(mark.mark)
            else:
                cri[mark.sub_criteria.criteria.name] += mark.mark
            total += mark.mark
        cri['totla_marks'] = total
            
        context = {
            'evaluation_date_from': '',
            'evaluation_date_to': '',
            'personal_no': soldier.personal_no,
            'rank': soldier.rank,
            'name': soldier.name,
            'appointment': soldier.appointment,
            'date_of_enrollment': soldier.date_of_enrollment,
            'last_promotion_date': soldier.last_promotion_date,
            'unit': soldier.unit,
            'medical_category': '',

            'IPFT_first_biannual': '',
            'IPFT_second_biannual': '',
            'RET': '',
            'DIV_order_letter_no_1': '',
            'DIV_order_letter_no_2': '',
            'DIV_order_letter_no_3': '',

            # Marks of different criteria 
            'criteria_name': cri,

            'fit_for_next_promotion': '',
            'fit_for_next_promotion_yes_text': '',
            'fit_for_next_promotion_no_text': '',
            
            'fit_for_being_instructor': '',
            'fit_for_being_instructor_yes_text': '',
            'fit_for_being_instructor_no_text': '',

            'fit_for_foreign_mission': '',
            'fit_for_foreign_mission_yes_text': '',
            'fit_for_foreign_mission_no_text': '',

            'recommendation_for_next_appt': '',
            'special_quality': '',
            'remarks_by_initiating_officer': '',

            'grade': '',
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, id):
        print(request.data)
        soldier = get_object_or_404(Soldier, pk=id)
        report = SoldierReport.objects.filter(soldier=soldier)
        report_form_serializer = ReportFormSerializer(data=request.data)
        report_form_serializer.is_valid(raise_exception=True)

        if report.count() == 0:
            SoldierReport.objects.create(
                soldier=soldier, 
                **report_form_serializer.validated_data
            )
        else:
            SoldierReport.objects.update(
                soldier=soldier, 
                **report_form_serializer.validated_data
            )
        
        return Response(
            {'message': 'Repost Data submitted successfully'}, 
            status=status.HTTP_201_CREATED
        )    


# Not view. 
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    open('test.html', 'w+').write(html)
    pdf = weasyprint.HTML('test.html').write_pdf()

    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse('<h3>We had some errors. try again.<h3>')

# View
def report_download(request, off_id, sol_id):
    soldier = get_object_or_404(Soldier, pk=sol_id)
    officer = get_object_or_404(Officer, pk=off_id)
    report = SoldierReport.objects.filter(soldier=soldier)
    print(report[0].evaluation_date_from)
    if(report.count() == 0):
        return HttpResponse("<h3>PDF not found</h3>", status=status.HTTP_404_NOT_FOUND)
    else:
        marks = SoldierMark.objects.filter(soldier=soldier)
        cri = {}
        total = 0
        for mark in marks:
            if mark.sub_criteria.criteria.name not in cri:
                cri[mark.sub_criteria.criteria.name] = int(mark.mark)
            else:
                cri[mark.sub_criteria.criteria.name] += mark.mark
            total += mark.mark
        cri['totla_marks'] = total

        context = {
            'pagesize': 'A4',
            'evaluation_date_from': report[0].evaluation_date_from,
            'evaluation_date_to': report[0].evaluation_date_to,
            'personal_no': soldier.personal_no,
            'rank': soldier.rank,
            'name': soldier.name,
            'appointment': soldier.appointment,
            'date_of_enrollment': soldier.date_of_enrollment,
            'last_promotion_date': soldier.last_promotion_date,
            'unit': soldier.unit,
            'medical_category': report[0].medical_category,

            'IPFT_first_biannual': bool(report[0].IPFT_first_biannual),
            'IPFT_second_biannual': bool(report[0].IPFT_second_biannual),
            'RET': bool(report[0].RET),
            'DIV_order_letter_no_1': report[0].DIV_order_letter_no_1,
            'DIV_order_letter_no_2': report[0].DIV_order_letter_no_2,
            'DIV_order_letter_no_3': report[0].DIV_order_letter_no_3,

            'criteria': cri,

            'fit_for_next_promotion': bool(report[0].fit_for_next_promotion),
            'fit_for_next_promotion_yes_text': report[0].fit_for_next_promotion_yes_text,
            'fit_for_next_promotion_no_text': report[0].fit_for_next_promotion_no_text,
            
            'fit_for_being_instructor': bool(report[0].fit_for_being_instructor),
            'fit_for_being_instructor_yes_text': report[0].fit_for_being_instructor_yes_text,
            'fit_for_being_instructor_no_text': report[0].fit_for_being_instructor_no_text,

            'fit_for_foreign_mission': bool(report[0].fit_for_foreign_mission),
            'fit_for_foreign_mission_yes_text': report[0].fit_for_foreign_mission_yes_text,
            'fit_for_foreign_mission_no_text': report[0].fit_for_foreign_mission_no_text,

            'recommendation_for_next_appt': report[0].recommendation_for_next_appt,
            'special_quality': report[0].special_quality,
            'remarks_by_initiating_officer': report[0].remarks_by_initiating_officer,

            'grade': report[0].grade,
            'grade_text': {
                'Outstanding (91-100)': 0,
                'Above Average (81-90)': 1,
                'High Average (71-80)': 2,
                'Average (61-70)': 3,
                'Below Average (51-60)': 4
            },

            'officer_ba': officer.ba_no,
            'officer_rank': officer.rank,
            'officer_name': officer.name,
            'officer_appt': officer.appointment,
            'officer_unit': officer.unit,
        }
        return render_to_pdf(
                'pdf_template.html',
                context
            )


def report_page(request):
    context = {
        'evaluation_date_from': '1-1-2020',
        'evaluation_date_to': '31-12-2020',
        'personal_no': 1,
        'rank': 1,
        'name': 'Soldier Name',
        'appointment': 'Appointment',
        'enrolement_date': '1-1-2020',
        'last_promotion_date': '1-1-2020',
        'unit': 'Unit',
        'medical_category': 'A',

        'IPFT_first_biannual': True,
        'IPFT_second_biannual': False,
        'RET': True,
        'DIV_order_letter_no_1': 'Some text1',
        'DIV_order_letter_no_2': 'Some text2',
        'DIV_order_letter_no_3': 'Some text3',

        # Marks of different criteria 
        'criteria': {
            'honesty': 4,
            'professional_efficiency': 3,
            'command_and_control': 7,
            'intelligence': 5,
            'dutifulness': 5,
            'professional_initiative': 4,
            'obedience': 6,
            'discipline': 6,
            'mentality_towards_senior': 9,
            'organizational_capabilities': 10,
            'total_marks': 56,
        },

        'fit_for_next_promotion': True,
        'fit_for_next_promotion_yes_text': '66.66',
        'fit_for_next_promotion_no_text': '33.33',
        
        'fit_for_being_instructor': False,
        'fit_for_being_instructor_yes_text': '66.66',
        'fit_for_being_instructor_no_text': '33.33',

        'fit_for_foreign_mission': True,
        'fit_for_foreign_mission_yes_text': '66.66',
        'fit_for_foreign_mission_no_text': '33.33',

        'recommendation_for_next_appt': 'Yes can be',
        'special_quality': 'Can Dance',
        'remarks_by_initiating_officer': 'Some remarks',

        'grade': 4,
        'grade_text': {
            'Outstanding (91-100)': 0,
            'Above Average (81-90)': 1,
            'High Average (71-80)': 2,
            'Average (61-70)': 3,
            'Below Average (51-60)': 4
        },

        'officer_ba': 12,
        'officer_rank': 'Officer Rank',
        'officer_name': 'Officer Name',
        'officer_appt': 'Officer Appt',
        'officer_unit': 'Officer Unit'
    }
    return render(request, 'pdf_template.html', context=context)