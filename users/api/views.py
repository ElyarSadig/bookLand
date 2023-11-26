from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from users.api.serializers import UserSignUpSerializer, LoginSerializer, SendEmailSerializer, VerifyEmailCodeSerializer,\
    ResetPasswordSerializer, PublisherAdditionalInfoSerializer, \
    PublisherImageUploadSerializer
from .api_result import APIResult
from users.api.utils import generate_random_code
from .jwt_token import generate_jwt_token
from .db_utils import UserActivityDBUtils, UserAuthenticationDBUtils, UserManagementDBUtils, UserRoleDBUtils
from users.api.email_utils import send_email_background_task
from .exceptions import *
from .jwt_token import publisher_login_required


class PublisherSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        response = APIResult()
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if UserManagementDBUtils.username_exists(username):
                raise UsernameAlreadyExistsError()

            if UserManagementDBUtils.email_exists(email):
                raise EmailAlreadyExistsError()

            user_id = UserManagementDBUtils.create_user(username, email, password, is_publisher=True)

            UserRoleDBUtils.assign_user_role(user_id, role_id=1)

            token = generate_jwt_token(user_id, role_id=1)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherDetailsUpdateView(GenericAPIView):
    serializer_class = PublisherAdditionalInfoSerializer

    @publisher_login_required
    def put(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PublisherAdditionalInfoSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            publications_name = serializer.validated_data["publications_name"]
            card_number = serializer.validated_data["card_number"]
            address = serializer.validated_data["address"]

            if UserManagementDBUtils.publications_name_exists(publications_name):
                raise PublicationsNameAlreadyExistsError()

            if UserManagementDBUtils.phone_number_exists(phone_number):
                raise PhoneNumberAlreadyExistsError()

            UserManagementDBUtils.update_publisher_info(user_id, phone_number, publications_name, card_number, address)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherImageUploadView(GenericAPIView):
    serializer_class = PublisherImageUploadSerializer

    @publisher_login_required
    def put(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PublisherImageUploadSerializer(data=request.data)
        if serializer.is_valid():

            publications_image = serializer.validated_data['publications_image']
            identity_image = serializer.validated_data['identity_image']

            UserManagementDBUtils.update_publisher_files(user_id, publications_image, identity_image)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        response = APIResult()
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if UserManagementDBUtils.username_exists(username):
                raise UsernameAlreadyExistsError()

            if UserManagementDBUtils.email_exists(email):
                raise EmailAlreadyExistsError()

            user_id = UserManagementDBUtils.create_user(username, email, password)

            UserRoleDBUtils.assign_user_role(user_id, 2)

            token = generate_jwt_token(user_id, role_id=2)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        response = APIResult()
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            identifier = serializer.validated_data['email_or_username']

            password = serializer.validated_data['password']

            user_id, stored_password, salt = UserAuthenticationDBUtils.get_user_password_from_username_or_email(identifier)

            if not user_id or not UserAuthenticationDBUtils.password_match(stored_password, password, salt):
                raise InvalidUserCredentialsError()

            role_id = UserRoleDBUtils.get_user_role_id(user_id)

            token = generate_jwt_token(user_id, role_id)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendSignUpEmailView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        response = APIResult()
        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            if UserManagementDBUtils.email_exists(email):
                raise EmailAlreadyExistsError()

            activation_code = generate_random_code()

            UserActivityDBUtils.create_user_activity_code(email, activation_code)

            subject = "فعال سازی حساب کاربری"
            template = "users/email_signup.html"
            send_email_background_task(subject, template, activation_code, email)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailCodeView(GenericAPIView):
    serializer_class = VerifyEmailCodeSerializer

    def post(self, request):
        response = APIResult()
        serializer = VerifyEmailCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']

            UserActivityDBUtils.validate_activation_code(email, activation_code)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetCodeView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        response = APIResult()
        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            if not UserManagementDBUtils.email_exists(email):
                raise EmailDoesNotExistError()

            code = generate_random_code()

            UserActivityDBUtils.create_user_activity_code(email, code)

            subject = "بازیابی رمز عبور"
            template = "users/reset_password_email.html"
            send_email_background_task(subject, template, code, email)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        response = APIResult()

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            password = serializer.validated_data['password']

            UserActivityDBUtils.validate_activation_code(email, activation_code)

            UserManagementDBUtils.update_user_password(password, email)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
