from django.urls import path
from apps.users.views import UserAPIView

urlpatterns = [
    path('register/', UserAPIView.as_view(), name='register')
]
