from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns= [
    path('signup/', SignupUserView.as_view(), name='signup'),

]