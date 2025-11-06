from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model= Skill
        fields = '__all__'


class UserSkillSerializer (serializers.ModelSerializer):
    class Meta:
        model= UserSkill
        fields = '__all__'

class MeetingSerializer (serializers.ModelSerializer):
    class Meta:
        model= Meeting
        fields = '__all__'
class CertificateSerializer (serializers.ModelSerializer):
    class Meta:
        model= Certificate
        fields = '__all__'

class ExperienceSerializer (serializers.ModelSerializer):
    class Meta:
        model= Experience
        fields = '__all__'
        
class UserProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields = '__all__'



class UserSerializer (serializers.ModelSerializer):
    certificates= CertificateSerializer(many= True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    class Meta:
        model= User
        fields = ['id' ,'username', 'first_name', 'last_name', 'email', 'certificates', 'experiences']
