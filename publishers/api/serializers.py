from rest_framework import serializers
from users.api.validation_utils import is_password_valid
from users.models import User
from accounts.models import WalletAction
from books.models import Book, BookCategory
from django.db import transaction


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
            'is_delete',
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


class CreateBookSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    language_id = serializers.IntegerField(write_only=True)
    publisher_id = serializers.IntegerField(required=False, write_only=True)
    book_cover_image = serializers.FileField(write_only=True, validators=[validate_file_type])
    demo_file = serializers.FileField(write_only=True, validators=[validate_pdf_file])
    original_file = serializers.FileField(write_only=True, validators=[validate_pdf_file])

    class Meta:
        model = Book
        fields = [
            'name', 'author_name', 'publisher_id', 'translator_name', 'released_date',
            'book_cover_image', 'price', 'description', 'number_of_pages',
            'language_id', 'category_id', 'demo_file', 'original_file'
        ]

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        with transaction.atomic():
            book = Book.objects.create(**validated_data, is_delete=True)
            BookCategory.objects.create(book=book, category_id=category_id, is_delete=False)
            description = validated_data["name"] + " " + "ایجاد کتاب"
            WalletAction.objects.create(
                action_type_id=2,
                user_id=validated_data["publisher_id"],
                amount=5000,
                is_successful=True,
                description=description
            )
        return book


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
    deposit = serializers.IntegerField(default=0)
    withdraw = serializers.IntegerField(default=0)