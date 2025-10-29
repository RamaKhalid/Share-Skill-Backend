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

class Home (APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # user = get_object_or_404(User)
            user = User.objects.all
            # profile = get_object_or_404(UserProfile, user_id=user.id)
            profile = UserProfile.objects.all
            user_serializer = UserSerializer(user, many=True)
            profile_serializer = UserSerializer(profile, many=True)
            # return Response(user_serializer.data,status=status.HTTP_200_OK)
            return Response({'user':user_serializer.data, 'profile':profile_serializer.data},status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

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
            

            profile_data= {
                'birth_date' : request.data.get("birth_date"),
                'level' : request.data.get("level"),
                'phone' : request.data.get("phone"),
                'user': request.data.get('user')
                }

            serializer = UserProfileSerializer(data = profile_data)
            if serializer.is_valid():
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password,
                    first_name = first_name,
                    last_name = last_name
                )
                serializer.save()
                queryset = UserProfile.objects.get(user=user.id)
                serializer = UserProfileSerializer(queryset)
                # return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.data,status=status.HTTP_201_CREATED,)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def get(self, request):
        try:
            skill = Skill.objects.all()
            serializer = SkillSerializer(skill, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def post (self, request):
        try:
            serializer = SkillSerializer(data=request.data)
            skill_id = request.data.get('id') 
            
            if Skill.objects.filter(id = skill_id).exists():
                    return Response(
                        {'error': "skill Already Exisits"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssociateSkill(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id, skill_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        skill = get_object_or_404(Skill, id=skill_id)
        user.skills.add(skill)

        skills_user_does_have = Skill.objects.filter(userprofile=user.id)
        skills_user_does_not_have = Skill.objects.exclude(
            id__in=user.skills.all().values_list("id")
        )

        return Response(
            {
                "skills_user_does_have": SkillSerializer(skills_user_does_have, many=True).data,
                "skills_user_does_not_have": SkillSerializer(
                    skills_user_does_not_have, many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )



class DissociateSkill(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id, skill_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        skill = get_object_or_404(Skill, id=skill_id)
        user.skills.remove(skill)

        # queryset = UserProfile.objects.get(user= user_id)

        skills_user_does_have = Skill.objects.filter(userprofile=user.pk)
        skills_user_does_not_have = Skill.objects.exclude(
            id__in=user.skills.all().values_list("id")
        )

        return Response(
            {
                "skills_user_does_have": SkillSerializer(skills_user_does_have, many=True).data,
                "skills_user_does_not_have": SkillSerializer(
                    skills_user_does_not_have, many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )



class Skilldetail (APIView):
    permission_classes = [AllowAny]
    def put (self, request, skill_id):
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
            queryset = get_object_or_404(Skill, id=skill_id)
            queryset.delete()

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
            certificate_id = request.data.get('id') 
            
            if Certificate.objects.filter(id = certificate_id).exists():
                    return Response(
                        {'error': "Certificate Already Exisits"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
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
    def put (self, request, cert_id):
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



class ExperienceIndex(APIView):
    permission_classes = [AllowAny]

    def get (self, request, user_id):
        try:
            queryset = Experience.objects.filter(owner=user_id)
            serializer = ExperienceSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post (self, request, user_id):
        try:
            serializer = ExperienceSerializer(data=request.data)
            experience_id = request.data.get('id') 
            
            if Experience.objects.filter(id = experience_id).exists():
                    return Response(
                        {'error': "Experience Already Exisits"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if serializer.is_valid():
                serializer.save()
                queryset = Experience.objects.filter(owner=user_id)
                serializer = ExperienceSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExperienceDetail(APIView):
    permission_classes = [AllowAny]
    def put (self, request, Experience_id):
        try:
            queryset = get_object_or_404(Experience, id = Experience_id)
            serializer = ExperienceSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, Experience_id):
        try:
            queryset = get_object_or_404(Experience, id=Experience_id)
            queryset.delete()
            return Response(
                {"message": f"Experience {Experience_id} has been deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class MeetingIndex(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            meeting = Meeting.objects.all()
            serializer = MeetingSerializer(meeting, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            serializer = MeetingSerializer(data=request.data)
            Meeting_id = request.data.get('id') 
            
            if Meeting.objects.filter(id = Meeting_id).exists():
                    return Response(
                        {'error': "Meeting Already Exisits"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MeetingDetail(APIView):
    permission_classes = [AllowAny]
    def put(self, request, meeting_id):
        try:
            meeting = get_object_or_404(Meeting, id = meeting_id)
            serializer = MeetingSerializer(meeting, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete (self, request, meeting_id):
        try:
            meeting = get_object_or_404(Meeting, id = meeting_id)
            meeting.delete()
            return Response({'message': f"Skill {meeting_id} has been deleted"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssociateMetting(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id, meeting_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        meeting = get_object_or_404(Meeting, id=meeting_id)
        user.meetings.add(meeting)

        meetings_user_does_have = Meeting.objects.filter(userprofile=user.id)
        meetings_user_does_not_have = Meeting.objects.exclude(
            id__in=user.meetings.all().values_list("id")
        )

        return Response(
            {
                "meetings_user_does_have": MeetingSerializer(meetings_user_does_have, many=True).data,
                "meetings_user_does_not_have": MeetingSerializer(
                    meetings_user_does_not_have, many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )
    

class DissociateMeeting(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id, meeting_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        meeting = get_object_or_404(Meeting, id=meeting_id)
        user.meetings.remove(meeting)

        meetings_user_does_have = Meeting.objects.filter(userprofile=user.id)
        meetings_user_does_not_have = Meeting.objects.exclude(
            id__in=user.meetings.all().values_list("id")
        )

        return Response(
            {
                "meetings_user_does_have": MeetingSerializer(meetings_user_does_have, many=True).data,
                "meetings_user_does_not_have": MeetingSerializer(
                    meetings_user_does_not_have, many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )





    
