from django.shortcuts import render
from rest_framework.views import APIView
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = User.objects.all()
            profile = UserProfile.objects.all()
            user_serializer = UserSerializer(user, many=True)
            profile_serializer = UserProfileSerializer(profile, many=True)
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
            
            if User.objects.filter(username=username ).exists():
                return Response(
                    {'error': "UserName Already Exisits"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if User.objects.filter(email=email ).exists():
                return Response(
                    {'error': "Email Already Exisits"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name = first_name,
                last_name = last_name
            )
            user_profile = UserProfile.objects.create(
               
                user = user
            )

            return Response({"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED,
        )            

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # profile_data= {
            #     'birth_date' : request.data.get("birth_date"),
            #     'level' : request.data.get("level"),
            #     'phone' : request.data.get("phone"),
            #     'user': user.id
            #     }

            # serializer = UserProfileSerializer(data = profile_data)
            # if serializer.is_valid():
            #     serializer.save()
            #     queryset = UserProfile.objects.get(user=user.id)
            #     serializer = UserProfileSerializer(queryset)
                # return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = User.objects.get(id = request.user)
        user.delete()
        return Response()



class UserProfileIndex(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user = User.objects.get(id= user_id)
            Profile = UserProfile.objects.get(user= user_id)
            Profile_serializer = UserProfileSerializer(Profile)
            user_serializer = UserSerializer(user)
            
            skills_user_teach = UserSkill.objects.filter(user_id=Profile.id , role = 'Teach')
            skills_user_learn = UserSkill.objects.filter(user_id=Profile.id , role = 'Learn')

            teach_skill= Skill.objects.filter (id__in=skills_user_teach.values_list('skill_id'))
            learn_skill= Skill.objects.filter (id__in=skills_user_learn.values_list('skill_id'))


            # skills_user_does_have = UserSkill.objects.filter(user_id= Profile.id)

            skills_user_does_not_have = Skill.objects.exclude(
                id__in=Profile.skills.all().values_list("id")
            )

            data = Profile_serializer.data
            data['skills_user_teach']= SkillSerializer( teach_skill, many=True).data
            data['skills_user_learn']=  SkillSerializer(learn_skill, many=True).data
            data["skills_user_does_not_have"] = SkillSerializer(skills_user_does_not_have, many=True).data

            return Response({'user':user_serializer.data, 'profile':data}, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # # use it after sign up immediately
    # def post(self, request, user_id):
    #     try:
    #         serializer = UserProfileSerializer(data = request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             queryset = UserProfile.objects.filter(user=user_id)
    #             serializer = UserProfileSerializer(queryset, many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as error:
    #         return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        
class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, user_id):
        try:
            queryset = get_object_or_404(User, id = user_id)
            serializer = UserSerializer(queryset, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class SkillIndex (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            skill = Skill.objects.all()
            serializer = SkillSerializer(skill, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post (self, request, user_id):
        try:
            serializer = SkillSerializer(data=request.data)
            
        
            if serializer.is_valid():
                skill= serializer.save()
                user = get_object_or_404(UserProfile, user_id=user_id)
                UserSkill.objects.create (user= user, skill= skill, role= request.data.get('role'))
                user_serializer = UserProfileSerializer(user)
                return Response({'data': serializer.data, 'skill user': user_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AssociateSkill(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, user_id, skill_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        skill = get_object_or_404(Skill, id=skill_id)

        # user.skills.add(skill)
        user.skills.add (skill, through_defaults ={'user':user, 'skill': skill, 'role': request.data.get('role')})
        user.save()
        serializer = UserProfileSerializer(user)


        skills_user_teach = UserSkill.objects.filter(user_id=user.id , role = 'Teach')
        skills_user_learn = UserSkill.objects.filter(user_id=user.id , role = 'Learn')   

        teach_skill= Skill.objects.filter (id__in=skills_user_teach.values_list('skill_id'))
        learn_skill= Skill.objects.filter (id__in=skills_user_learn.values_list('skill_id'))

        skills_user_does_not_have = Skill.objects.exclude(
            id__in=user.skills.all().values_list("id")
        )
        return Response(
            {
                'skills_user_teach':SkillSerializer( teach_skill, many=True).data,
                'skills_user_learn': SkillSerializer(learn_skill, many=True).data,
                "skills_user_does_not_have": SkillSerializer(skills_user_does_not_have, many=True).data,
             },
                status=status.HTTP_200_OK,
            ) 



class DissociateSkill(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, user_id, skill_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        skill = get_object_or_404(Skill, id=skill_id)
        user.skills.remove(skill)

        
        skills_user_teach = UserSkill.objects.filter(user_id=user.id , role = 'Teach')
        skills_user_learn = UserSkill.objects.filter(user_id=user.id , role = 'Learn')   
   
        teach_skill= Skill.objects.filter (id__in=skills_user_teach.values_list('skill_id'))
        learn_skill= Skill.objects.filter (id__in=skills_user_learn.values_list('skill_id'))

        skills_user_does_not_have = Skill.objects.exclude(
            id__in=user.skills.all().values_list("id")
        )
        return Response(
            {
                'skills_user_teach':SkillSerializer( teach_skill, many=True).data,
                'skills_user_learn': SkillSerializer(learn_skill, many=True).data,
                "skills_user_does_not_have": SkillSerializer(skills_user_does_not_have, many=True).data,
             },
                status=status.HTTP_200_OK,
            ) 



class Match (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user = get_object_or_404(UserProfile, user_id=user_id)

            skills_user_teach = UserSkill.objects.filter(user_id=user.id , role = 'Teach')
            skills_user_learn = UserSkill.objects.filter(user_id=user.id , role = 'Learn') 
            users_can_teach_you = UserSkill.objects.filter(skill__in =[s.skill for s in skills_user_learn], role ='Teach')
            users_learn_by_you = UserSkill.objects.filter(user_id__in=users_can_teach_you.values_list('user_id'),role = 'Learn')
            
            users_can_teach_and_learn_by_you =users_learn_by_you.filter(
                skill__in =[s.skill for s in skills_user_teach])
            
            user_profile_skill= UserProfile.objects.filter (id__in=users_can_teach_and_learn_by_you.values_list('user_id'))
            user_skill= User.objects.filter (id__in=user_profile_skill.values_list('user_id'))
            Learn_skill_data= Skill.objects.filter (id__in=users_can_teach_and_learn_by_you.values_list('skill_id'))
            teach_skill_data= Skill.objects.filter (id__in=users_can_teach_you.values_list('skill'))
                        
            return Response({'teach_skill_data': SkillSerializer(teach_skill_data, many=True).data,
                'Learn_skill_data':SkillSerializer(Learn_skill_data, many=True).data,
                'user_match': UserSerializer(user_skill, many=True).data,
                'profile_user':UserProfileSerializer(user_profile_skill, many=True).data,
                'users_can_teach_and_learn_by_you': UserSkillSerializer(users_can_teach_and_learn_by_you, many=True).data,
                'users_can_teach_you': UserSkillSerializer(users_can_teach_you, many=True).data}, status=status.HTTP_200_OK,)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatchOneSkill(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,user_id, skill_id):
        try:
            user = get_object_or_404(UserProfile, user_id=user_id)
            # skill_user_want_to_learn = skills_user_learn.filter(skill_id=skill_id)
            skill_user_learn = UserSkill.objects.filter(skill_id=skill_id , role = 'Learn')

            skill_user_teach =UserSkill.objects.filter(user_id=user.id , role = 'Teach')

            users_can_teach_you = UserSkill.objects.filter(skill__in =[s.skill for s in skill_user_learn], role ='Teach')

            users_want_to_learn = UserSkill.objects.filter(user_id__in=users_can_teach_you.values_list('user_id'),role = 'Learn')

            users_can_teach_and_learn_by_you =users_want_to_learn.filter(skill__in =[s.skill for s in skill_user_teach])

            user_profile_skill= UserProfile.objects.filter (id__in=users_can_teach_and_learn_by_you.values_list('user_id'))
   
            user_skill= User.objects.filter (id__in=user_profile_skill.values_list('user_id'))
 
            Learn_skill_data= Skill.objects.filter (id__in=users_can_teach_and_learn_by_you.values_list('skill_id'))
  
            teach_skill_data= Skill.objects.filter (id__in=users_can_teach_you.values_list('skill'))

            return Response({'teach_skill_data': SkillSerializer(teach_skill_data, many=True).data,
                'Learn_skill_data':SkillSerializer(Learn_skill_data, many=True).data,
                'user_match': UserSerializer(user_skill, many=True).data,
                'profile_user':UserProfileSerializer(user_profile_skill, many=True).data,
                'users_can_teach_and_learn_by_you': UserSkillSerializer(users_can_teach_and_learn_by_you, many=True).data,
                'users_can_teach_you': UserSkillSerializer(users_can_teach_you, many=True).data}, status=status.HTTP_200_OK,)
        except Exception as error:
                    return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Skilldetail (APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def put (self, request, cert_id):
        try:
            queryset = get_object_or_404(Certificate, id = cert_id)
            serializer = CertificateSerializer(queryset, data=request.data)
            certificate_id = request.data.get('owner')
            if serializer.is_valid():
                serializer.save()
                queryset = Certificate.objects.filter(owner=certificate_id)
                serializer = CertificateSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    def put (self, request, Experience_id):
        try:
            queryset = get_object_or_404(Experience, id = Experience_id)
            serializer = ExperienceSerializer(queryset, data=request.data)
            experience_id = request.data.get('owner')
            if serializer.is_valid():
                serializer.save()
                queryset = Experience.objects.filter(owner=experience_id)
                serializer = ExperienceSerializer(queryset, many=True)
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
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            username=[]
            user_profile = get_object_or_404(UserProfile, user_id=user_id)
            #take all the meeting that the user have 
            meeting = user_profile.meetings.all() 
            
            #Look for other users that have the same meeting id 
            participant_meeting= Meeting.objects.filter(id__in= meeting.values_list('id', flat=True))

            #Take the Userprofile data For the other useres that share the same meeting as you (to take the User ID)
            users_with_this_meeting_list=UserProfile.objects.filter(meetings__in= participant_meeting.values_list('id', flat=True))

            # Take the Users from the Userprofile to save the username later
            user_ids = User.objects.filter( id__in= users_with_this_meeting_list.values_list('user', flat=True))

            #only take the other user (participant) ond leave the your data
            participant = user_ids.exclude(id =user_id )
            participant_serializer=UserSerializer(participant,many=True).data

            
            meeting_serializer = MeetingSerializer(meeting, many=True).data
            #Take the username from the participent to join it later with the meeting
            for data in participant_serializer:
                username.append(data['username'])
                
            #Give the meeting thier participent
            data=meeting_serializer
            meeting_count = len(data)
            username_count = len(username)
            limit = min(meeting_count, username_count)

            for i in range(limit):
                meeting = data[i]
                name = username[i]
                meeting['participant'] = name

            return Response({ 'meeting':data, })
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def post(self, request,user_id):
    #     try:
    #         serializer = MeetingSerializer(data=request.data)
    #         if serializer.is_valid():
    #             meeting_serializer= serializer.save().id
    #             user = get_object_or_404(UserProfile, user_id=user_id)
    #             meeting = get_object_or_404(Meeting, id=meeting_serializer)
    #             user.meetings.add(meeting)
    #             meetings_user_does_have = Meeting.objects.filter(userprofile=user.id)
    #             meetings_serializer= MeetingSerializer(meetings_user_does_have, many=True).data
    #             return Response(
    #                 meetings_serializer,
    #                 status=status.HTTP_200_OK,
    #             )
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as error:
    #         return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self, request, user_id):
        try:
            username=[]
            serializer = MeetingSerializer(data=request.data)
            if serializer.is_valid():
                meeting = serializer.save()  
                
                # Add creator
                creator = get_object_or_404(UserProfile, user_id=user_id)
                creator.meetings.add(meeting)
            
                # Add participants
                # user = User.objects.all()
                participant_username = request.data.get('participant_username')
                users = User.objects.get(username__iexact  = participant_username)
            
                if users.id != user_id:
                    participant = get_object_or_404(UserProfile, user_id=users.id)
                    participant.meetings.add(meeting)
                
                meetings_user_does_have = creator.meetings.all()
                meetings_serializer= MeetingSerializer(meetings_user_does_have, many=True).data
                
                the_new_participant_meeting= participant.meetings.filter(id__in= meetings_user_does_have.values_list('id', flat=True))
                participant_data =UserSerializer(users).data

                participant_meeting= Meeting.objects.filter(id__in= meetings_user_does_have.values_list('id', flat=True))

                #Take the Userprofile data For the other useres that share the same meeting as you (to take the User ID)
                users_with_this_meeting_list=UserProfile.objects.filter(meetings__in= participant_meeting.values_list('id', flat=True))

                # Take the Users from the Userprofile to save the username later
                user_ids = User.objects.filter( id__in= users_with_this_meeting_list.values_list('user', flat=True))

                #only take the other user (participant) ond leave the your data
                participant = user_ids.exclude(id =user_id )
                participant_serializer=UserSerializer(participant,many=True).data

                
                meeting_serializer = MeetingSerializer(meetings_user_does_have, many=True).data
                #Take the username from the participent to join it later with the meeting
                for data in participant_serializer:
                    username.append(data['username'])
                    
                #Give the meeting thier participent
                data=meeting_serializer
                meeting_count = len(data)
                username_count = len(username)
                limit = min(meeting_count, username_count)

                for i in range(limit):
                    meeting = data[i]
                    name = username[i]
                    meeting['participant'] = name

                return Response({ 'meeting':data, })

                # users_with_this_meeting_list=UserProfile.objects.filter(meetings__in= the_new_participant_meeting.values_list('id', flat=True))
                # user_ids = User.objects.filter( id__in= users_with_this_meeting_list.values_list('user', flat=True))
                # # y=UserProfileSerializer(users_with_this_meeting,many=True).data
                # participant = user_ids.exclude(id =user_id )
                # users_with_this_meeting=UserSerializer(participant,many=True).data

                # for data in users_with_this_meeting:
                #     username.append(data['username'])
                #     print(username)

                # data=the_new_participant_meeting
                # for i in range(len(data)):
                #     if i < len(username):
                #         data[i]['participant'] = username[i]


                # # for met in data:
                
                # #     met['participant']=username


                # return Response(
                #     {'meeting':meetings_serializer,
                #      'participant':participant_data},
                #     status=status.HTTP_200_OK,
                # )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    

        

class MeetingDetail(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id, meeting_id):
        user = get_object_or_404(UserProfile, user_id=user_id)
        meeting = get_object_or_404(Meeting, id=meeting_id)
        user.meetings.add(meeting)

        meetings_user_does_have = user.meetings.all()
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
    permission_classes = [IsAuthenticated]

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





    
