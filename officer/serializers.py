from rest_framework import serializers

from clerk.models import Clerk
from .models import Officer
from django.contrib.auth.models import User

from clerk.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer


class OfficerCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Officer
        fields = ('user', 'ba_no', 'name', 'password', 'rank', 'address', 
                    'unit', 'subunit', 'appointment', 'starting_date', 'contact')

    def create(self, validated_data):
        userData = validated_data.pop('user', None)
        user = User.objects.create(
            username=userData['username'],
            email=userData['email'],
        )
        user.set_password(userData['password'])
        user.save()
        validated_data['user'] = user

        # Set new officer as active and end the last officer
        subunit = validated_data.get('subunit', None)
        if subunit:
            cc = Officer.objects.filter(subunit=subunit)
            if cc.count() > 0:
                cc.latest('starting_date').end_officer_duty()
            
        
        return Officer.objects.create(**validated_data)


class OfficerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Officer
        fields = ('user', 'id', 'ba_no', 'name', 'password', 'rank', 'address', 
                    'unit', 'subunit', 'appointment', 'starting_date', 'ending_date', 'contact', 'profile_pic')
    

class OfficerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Officer
        fields = ('user', 'ba_no', 'name', 'password', 'rank', 'address', 
                    'unit', 'subunit', 'appointment', 'contact')
    

    def update(self, instance, validated_data):
        user = instance.user
        userdata = validated_data.pop('user', None)
        user.username = userdata.get('username', user.username)
        user.email = userdata.get('email', user.email)
        user.save()

        instance.user = user
        instance.name = validated_data.get('name', instance.name)
        instance.ba_no = validated_data.get('ba_no', instance.ba_no)
        instance.password = validated_data.get('password', instance.password)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.address = validated_data.get('address', instance.address)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.subunit = validated_data.get('subunit', instance.subunit)
        instance.appointment = validated_data.get('appointment', instance.appointment)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.save()
        return instance