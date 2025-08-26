from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
import random
import string

from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmationSerializer
from .models import ConfirmationCode

User = get_user_model()


class AuthorizationAPIView(APIView):

    @swagger_auto_schema(request_body=AuthValidateSerializer)
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Get or create auth token
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    @swagger_auto_schema(request_body=RegisterValidateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()  # uses serializer.create()

            # Create a random 6-digit confirmation code
            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
        )


class ConfirmUserAPIView(APIView):

    @swagger_auto_schema(request_body=ConfirmationSerializer)
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Delete confirmation code and return token
            ConfirmationCode.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User account successfully activated',
                'key': token.key
            }
        )
