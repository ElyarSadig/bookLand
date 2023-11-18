from rest_framework import serializers
from users.api.validation_utils import password_match


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(write_only=True)


