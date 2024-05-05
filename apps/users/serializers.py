from rest_framework import serializers

from apps.users.models import CustomUser


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, min_length=8)

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exists")
        return email


class ResendConfirmationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, min_length=8, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, min_length=8, required=True)


class PasswordResetSearchUserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, min_length=8)
