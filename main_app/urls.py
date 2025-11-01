from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns= [
    path('home/', Home.as_view(), name='home'),
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:user_id>/', UserProfileIndex.as_view(), name='profile'),
    path('user/<int:user_id>/', UserUpdate.as_view(), name='User_update'),
    path('skills/<int:user_id>', SkillIndex.as_view(), name='skill'),
    # path('skills/<int:skill_id>/', Skilldetail.as_view(), name='Skill_detail'),
    path('profile/<int:user_id>/associate-skill/<int:skill_id>/',AssociateSkill.as_view(), name= 'assoc_skill'),
    path('profile/<int:user_id>/dissociate-skill/<int:skill_id>/',DissociateSkill.as_view(), name= 'deassoc_skill'),
    path('profile/<int:user_id>/certificate/', CertificateIndex.as_view(), name='certificate_Index'),
    path('profile/certificate/<int:cert_id>/', CertificateDetail.as_view(), name='certificate_detail'),
    path('profile/<int:user_id>/experience/', ExperienceIndex.as_view(), name='experience_Index'),
    path('profile/experience/<int:Experience_id>/', ExperienceDetail.as_view(), name='experience_detail'),
    path('meetings/', MeetingIndex.as_view(), name='all_meeting'),
    path('meeting/<int:meeting_id>/', MeetingDetail.as_view(), name='meeting'),
    path('profile/<int:user_id>/associate-meeting/<int:meeting_id>/',AssociateMetting.as_view(), name= 'assoc_meeting'),
    path('profile/<int:user_id>/dissociate-meeting/<int:meeting_id>/',DissociateMeeting.as_view(), name= 'deassoc_meeting'),
    path('match/<int:user_id>', Match.as_view(), name= 'Match')
]