from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user-registration'),
    path('authorization/', AuthorizationAPIView.as_view(), name='user-authorization'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='user-confirm'),
]