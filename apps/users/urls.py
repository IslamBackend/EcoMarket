from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import RegisterAPIView, LoginAPIView, VerifyOtpAPIview, ChangePasswordAPIView, \
    ResetPasswordSendEmailAPIView, PasswordTokenCode, PasswordResetNewPassword

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('confirm/', VerifyOtpAPIview.as_view(), name='confirm'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordSendEmailAPIView.as_view(), name='reset_password_send_email'),
    path('reset-password/verify/', PasswordTokenCode.as_view(), name='password_token_code'),
    path('reset-password/new/<str:code>/', PasswordResetNewPassword.as_view(), name='password_reset_new_password'),
]
