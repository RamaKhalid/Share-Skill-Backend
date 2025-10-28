from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns= [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('profile/<int:user_id>/', UserProfileIndex.as_view(), name='profile'),
    path('profile/<int:user_id>/skill/', SkillIndex.as_view(), name='skill'),
    path('profile/<int:user_id>/skill/<int:skill_id>/', Skilldetail.as_view(), name='Skill_detail'),
    path('profile/<int:user_id>/associate-skill/<int:skill_id>/',AssociateSkill.as_view(), name= 'assoc_skill'),
    path('profile/<int:user_id>/certificate/', CertificateIndex.as_view(), name='certificate_Index'),
    path('profile/<int:user_id>/certificate/<int:cert_id>/', CertificateDetail.as_view(), name='certificate_detail'),

]