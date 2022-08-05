from rest_framework import serializers
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'position', 'is_staff']
        read_only_fields = ['id', 'email', 'is_staff']

