from rest_framework import serializers
from users.api.validation_utils import is_password_valid
from books.models import Book
from users.models import User
from accounts.models import WalletAction


def validate_file_type(value):
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']

    if value.content_type not in allowed_types:
        raise serializers.ValidationError("Invalid file type. Only JPEG, JPG and PNG files are allowed.")


def validate_pdf_file(value):
    allowed_types = ['application/pdf']

    if value.content_type not in allowed_types:
        raise serializers.ValidationError("Invalid file type. Only PDF files are allowed.")


class BookSerializer(serializers.ModelSerializer):
    count_of_sold = serializers.IntegerField()
    income = serializers.IntegerField()

    class Meta:
        model = Book
        fields = [
            'id',
            'name',
            'author_name',
            'translator_name',
            'released_date',
            'book_cover_image',
            'price',
            'number_of_pages',
            'count_of_sold',
            'income'
        ]


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


class PublisherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "phone_number2", "address", "identity_image", "card_number",
                  "publications_name", "publications_image"]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True, 'allow_null': True},
            'phone_number2': {'required': False, 'allow_blank': True, 'allow_null': True},
            'address': {'required': False, 'allow_blank': True, 'allow_null': True},
            'card_number': {'required': False, 'allow_blank': True, 'allow_null': True},
            'publications_image': {'required': False, 'allow_blank': True, 'allow_null': True}
        }


class WalletActionSerializer(serializers.ModelSerializer):
    action_type = serializers.CharField(source='action_type.action_type', read_only=True)

    class Meta:
        model = WalletAction
        fields = [
            'id',
            'action_type',
            'amount',
            'is_successful',
            'description',
            'created_date'
        ]


class WalletActionSummarySerializer(serializers.Serializer):
    deposit = serializers.IntegerField()
    withdraw = serializers.IntegerField()