from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.

User = get_user_model()

class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username= request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username:
            return Response(
                {"error": "Please provide an username"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not first_name:
            return Response(
                {"error": "Please provide a first name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not last_name:
            return Response(
                {"error": "Please provide a Last name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if  not password :
            return Response(
                {"error": "Please provide a password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if  not email:
            return Response(
                {"error": "Please provide an email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': "User Already Exisits"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name = first_name,
            last_name = last_name
        )

        return Response(
            {"id": user.id, "username": user.username, "first_name":first_name, "last_name":last_name, "email": user.email, },
            status=status.HTTP_201_CREATED,
        )
        

        


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



    
