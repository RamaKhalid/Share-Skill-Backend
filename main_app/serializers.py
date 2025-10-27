from rest_framework import serializers
from .models import *

class UserProfilePerializer (serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        feilds = '__all__'

class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model= Skill
        feilds = '__all__'