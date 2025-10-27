from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields = '__all__'

class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model= Skill
        fields = '__all__'

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
