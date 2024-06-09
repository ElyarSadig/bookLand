from rest_framework import serializers
from users.api.validation_utils import is_password_valid


def validate_file_type(value):
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']

    if value.content_type not in allowed_types:
        raise serializers.ValidationError("Invalid file type. Only JPEG, JPG and PNG files are allowed.")


def validate_pdf_file(value):
    allowed_types = ['application/pdf']

    if value.content_type not in allowed_types:
        raise serializers.ValidationError("Invalid file type. Only PDF files are allowed.")


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


class UpdatePublisherProfileSerializer(serializers.Serializer):
    address = serializers.CharField(required=False, default="")
    phone_number2 = serializers.CharField(required=False, max_length=11, default="")
    publications_image = serializers.CharField(required=False, default="")
    card_number = serializers.CharField(required=False, default="", max_length=16, min_length=16)


class CreateBookSerializer(serializers.Serializer):
    book_name = serializers.CharField(max_length=255)
    author_name = serializers.CharField(max_length=255)
    translator_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    released_date = serializers.IntegerField()
    book_cover_image = serializers.FileField(validators=[validate_file_type])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_blank=True, required=False)
    number_of_pages = serializers.IntegerField()
    language_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    book_demo_file = serializers.FileField(allow_null=True, validators=[validate_pdf_file])
    book_original_file = serializers.FileField(allow_null=True, validators=[validate_pdf_file])


