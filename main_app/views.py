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
        try:
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

            # profile_data= {
            #     'birth_date' : request.data.get("birth_date"),
            #     'level' : request.data.get("level"),
            #     'phone' : request.data.get("phone"),
            #     'user': request.data.get('user')
            #     }

            # serializer = UserProfileSerializer(data = profile_data)
            # if serializer.is_valid():
            #     serializer.save()
            #     queryset = UserProfile.objects.get(user=user.id)
            #     serializer = UserProfileSerializer(queryset, many=True)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            return Response(
                {"id": user.id, "username": user.username, "first_name":first_name, "last_name":last_name, "email": user.email, },
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserProfileIndex(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        try:
            queryset = UserProfile.objects.get(user= user_id)
            serializer = UserProfileSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # use it after sign up immediately
    def post(self, request, user_id):
        try:
            serializer = UserProfileSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = UserProfile.objects.filter(user=user_id)
                serializer = UserProfileSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, user_id):
        try:
            queryset = get_object_or_404(UserProfile, user = user_id)
            serializer = UserProfileSerializer(queryset, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class SkillIndex (APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):

        try:
            queryset = Skill.objects.filter(owner=user_id)
            serializer = SkillSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def post (self, request, user_id):
    # When we make a GET request, return All of the feedings that relate to a specific cat
        try:
            serializer = SkillSerializer(data=request.data)
        # if Skill.objects.filter(=id).exists():
        #         return Response(
        #             {'error': "skill Already Exisits"},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        
            if serializer.is_valid():
                serializer.save()
                queryset = Skill.objects.filter(owner=user_id)
                serializer = SkillSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Skilldetail (APIView):
    permission_classes = [AllowAny]
    def put (self, request, user_id, skill_id):
        try:
            queryset = get_object_or_404(Skill, id = skill_id)
            serializer = SkillSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, skill_id):
        try:
            # Get a cat or return a 404
            queryset = get_object_or_404(Skill, id=skill_id)
            # delete the cat
            queryset.delete()
            # return a response
            return Response(
                {"message": f"Skill {skill_id} has been deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CertificateIndex(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            queryset = Certificate.objects.filter(owner=user_id)
            serializer = CertificateSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post (self, request, user_id):
        try:
            serializer = CertificateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Certificate.objects.filter(owner=user_id)
                serializer = CertificateSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
        

class CertificateDetail(APIView):
    permission_classes = [AllowAny]
    def put (self, request, user_id, cert_id):
        try:
            queryset = get_object_or_404(Certificate, id = cert_id)
            serializer = CertificateSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #review it tommorw
    def delete(self, request, cert_id):
        try:
            queryset = get_object_or_404(Certificate, id=cert_id)
            queryset.delete()
            return Response(
                {"message": f"Certificate {cert_id} has been deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





    
