from rest_framework import serializers


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


class PublisherSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20)
    publications_name = serializers.CharField(max_length=200)
    card_number = serializers.CharField(max_length=50)
    identity_image = serializers.CharField(max_length=300)
    publications_image = serializers.CharField(max_length=300)
    address = serializers.CharField(max_length=500)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.CharField(required=False, max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")

        if not (username or email):
            raise serializers.ValidationError("You must provide either a username or an email.")

        if username and email:
            raise serializers.ValidationError("You can't provide both a username and an email. Choose one.")

        return attrs


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)


class VerifyEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    activation_code = serializers.CharField(required=True, max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    activation_code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
