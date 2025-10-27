from rest_framework import serializers
from .models import *

class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model= Skill
        feilds = '__all__'