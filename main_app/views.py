from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.

class SkillIndex (APIView):
    def get(self, request, user_id):
        try:
            queryset = Skill.objects.filter(user=user_id)
            serializer = SkillSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    def post (self, request, user_id):
    # When we make a GET request, return All of the feedings that relate to a specific cat
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Skill.objects.filter(user=user_id)
            serializer = SkillSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
