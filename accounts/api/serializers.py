from rest_framework import serializers
from users.api.validation_utils import is_password_valid


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        error_message = is_password_valid(password=attrs["new_password"])

        if len(error_message) != 0:
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidPassword",
                    "error_message": error_message,
                    "errors": ""
                },
                "data": "",
            })

        return attrs


class UserBookmarkSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()


