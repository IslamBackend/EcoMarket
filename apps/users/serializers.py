from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'address', 'phone')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
