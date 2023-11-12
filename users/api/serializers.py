from rest_framework import serializers
from users.api.validation_utils import is_email_valid, is_username_valid, password_match, validate_iranian_phone_number


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):

        if not is_username_valid(attrs["username"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidUsername",
                    "error_message": "نام کاربری نا معتبر",
                    "errors": ""
                },
                "data": "",
            })

        if not is_email_valid(attrs["email"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidEmail",
                    "error_message": "ایمیل نامعتبر",
                    "errors": ""
                },
                "data": "",
            })

        if not password_match(attrs["password"], attrs["password2"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "PasswordsDoNotMatch",
                    "error_message": "پسورد مطابقت ندارد",
                    "errors": ""
                },
                "data": "",
            })

        return attrs


class PublisherSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20)
    publications_name = serializers.CharField(max_length=200)
    publications_image = serializers.CharField(max_length=300)
    card_number = serializers.CharField(max_length=50)
    identity_image = serializers.CharField(max_length=300)
    address = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):

        if not is_username_valid(attrs["username"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidUsername",
                    "error_message": "نام کاربری نا معتبر",
                    "errors": ""
                },
                "data": "",
            })

        if not is_email_valid(attrs["email"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidEmail",
                    "error_message": "ایمیل نامعتبر",
                    "errors": ""
                },
                "data": "",
            })

        if not password_match(attrs["password"], attrs["password2"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "PasswordsDoNotMatch",
                    "error_message": "پسورد مطابقت ندارد",
                    "errors": ""
                },
                "data": "",
            })

        if not validate_iranian_phone_number(attrs["phone_number"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidPhoneNumber",
                    "error_message": "شماره تلفن معتبر نمی باشد",
                    "errors": ""
                },
                "data": "",
            })

        return attrs


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_username = attrs["email_or_username"]

        if not is_email_valid(email_or_username):

            if not is_username_valid(email_or_username):

                raise serializers.ValidationError({
                    "result": {
                        "error_code": "InvalidCredentials",
                        "error_message": "ایمیل نام کاربری نامعتبر",
                        "errors": ""
                    },
                    "data": "",
                })

        return attrs


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)


class VerifyEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    activation_code = serializers.CharField(required=True, max_length=10)

    def validate(self, attrs):

        if len(attrs['activation_code']) != 6:
            raise serializers.ValidationError({
                "result": {
                    "error_code": "InvalidActivationCode",
                    "error_message": "کد نامعتبر",
                    "errors": ""
                },
                "data": "",
            })

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    activation_code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):

        if not password_match(attrs["password"], attrs["password2"]):
            raise serializers.ValidationError({
                "result": {
                    "error_code": "PasswordsDoNotMatch",
                    "error_message": "پسورد مطابقت ندارد",
                    "errors": ""
                },
                "data": "",
            })

        return attrs
