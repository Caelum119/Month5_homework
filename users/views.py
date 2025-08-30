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
from .redis_codes import get_confirmation_code, delete_confirmation_code


from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmationSerializer
from .models import ConfirmationCode

User = get_user_model()


class AuthorizationAPIView(APIView):

    @swagger_auto_schema(request_body=AuthValidateSerializer)
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    @swagger_auto_schema(request_body=RegisterValidateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()  

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
    def post(self, request):
        user_id = request.data.get("user_id")
        code = request.data.get("code")

        if not user_id or not code:
            return Response({"error": "Missing parameters"}, status=400)

        stored_code = get_confirmation_code(user_id)

        if stored_code != code:
            return Response({"error": "Invalid code"}, status=400)

        delete_confirmation_code(user_id)
        return Response({"success": "User confirmed"})

