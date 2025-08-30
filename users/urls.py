from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView
from users.oauth import GoogleLoginAPIView





urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user-registration'),
    path('authorization/', AuthorizationAPIView.as_view(), name='user-authorization'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='user-confirm'),
    path('google-login/', GoogleLoginAPIView.as_view()),


]