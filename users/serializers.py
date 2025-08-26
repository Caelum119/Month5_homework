from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterValidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'full_name', 'birth_date']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            birth_date=validated_data.get('birth_date', None)
        )
        user.is_active = False  
        user.save()
        return user


class AuthValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is not activated yet.")
        data['user'] = user
        return data



class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        from .models import ConfirmationCode
        try:
            confirmation = ConfirmationCode.objects.get(
                user_id=data['user_id'],
                code=data['code']
            )
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid confirmation code")
        data['confirmation'] = confirmation
        return data
