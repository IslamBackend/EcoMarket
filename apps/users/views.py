from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.email import send_confirmation_email, send_password_reset_email, generate_random_code
from apps.users.models import CustomUser, PasswordResetToken
from apps.users.serializers import RegisterSerializer, LoginSerializer, VerifySerializer, ChangePasswordSerializer, \
    PasswordResetSearchUserSerializer, PasswordResetCodeSerializer, PasswordResetNewPasswordSerializer, \
    ResendConfirmationEmailSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.create_user(**serializer.validated_data)
        send_confirmation_email(user)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class ResendConfirmationEmailAPIView(APIView):
    def post(self, request):
        serializer = ResendConfirmationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response(
                {'error': 'User with provided email does not exist'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_active:
            return Response(
                {'message': 'User is already active'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_confirmation_email(user)

        return Response(
            {'message': 'Confirmation email sent successfully'},
            status=status.HTTP_200_OK,
        )


class VerifyOtpAPIview(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response(
                {'error': 'User does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.otp != otp:
            return Response(
                {'error': 'Invalid OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.otp = None
        user.save()

        return Response(
            {'message': 'Account successfully verified.'},
            status=status.HTTP_200_OK
        )


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'Successfully logged in.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': 'Invalid credentials.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {'error': 'Old password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password == old_password:
            return Response(
                {'error': 'New password should not match old password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'message': 'Password successfully changed.'},
            status=status.HTTP_200_OK
        )


class ResetPasswordSendEmailAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSearchUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response(
                {'error': 'User with provided email address not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        password_reset_token = PasswordResetToken.objects.filter(user=user).first()

        if password_reset_token and password_reset_token.time > timezone.now():
            return Response(
                {'error': 'A password reset token already exists and has not expired.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_code = generate_random_code()
        expiration_time = timezone.now() + timezone.timedelta(minutes=15)

        if password_reset_token:
            password_reset_token.code = new_code
            password_reset_token.time = expiration_time
            password_reset_token.save()
        else:
            PasswordResetToken.objects.create(
                user=user,
                code=new_code,
                time=expiration_time,
            )

        send_password_reset_email(user.email, new_code)

        return Response(
            {'detail': 'A new password reset code has been sent to your email.'},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCode(APIView):
    def post(self, request):
        serializer = PasswordResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        try:
            PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid password reset code or code expiration time has passed.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {'detail': 'Code validated successfully.'},
            status=status.HTTP_200_OK
        )


class PasswordResetNewPassword(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = kwargs.get('code')
        print(code)
        new_password = serializer.validated_data.get('password')

        try:
            password_reset_token = PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid password reset code or code expiration time has passed.'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = password_reset_token.user
        user.set_password(new_password)
        user.save()

        password_reset_token.delete()

        return Response(
            {'detail': 'Password successfully reset.'},
            status=status.HTTP_200_OK
        )
