from rest_framework import serializers
from users.api.validation_utils import is_password_valid
from users.models import User
from books.models import Book


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        error_message = is_password_valid(password=attrs["new_password"])

        if len(error_message) != 0:
            raise serializers.ValidationError({
                "result": {
                    "error_message": error_message,
                    "errors": ""
                },
                "data": "",
            })

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "username"]


class UserBookSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(source='publisher.publications_name')
    language = serializers.CharField(source='language.name')

    class Meta:
        model = Book
        fields = [
            'id', 'publisher', 'name', 'author_name', 'translator_name',
            'released_date', 'book_cover_image', 'price', 'number_of_pages',
            'language'
        ]


class UserBookmarkSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(source='publisher.publications_name')
    language = serializers.CharField(source='language.name')

    class Meta:
        model = Book
        fields = [
            'id', 'publisher', 'name', 'author_name', 'translator_name',
            'released_date', 'book_cover_image', 'price',
            'number_of_pages', 'language'
        ]



