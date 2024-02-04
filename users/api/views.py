from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from users.api.serializers import UserSignUpSerializer, LoginSerializer, SendEmailSerializer, VerifyEmailCodeSerializer,\
    ResetPasswordSerializer, PublisherAdditionalInfoSerializer, \
    PublisherImageUploadSerializer
from .api_result import APIResult
from .jwt_token import generate_jwt_token
from users.api.email_utils import send_email_background_task
from .jwt_token import publisher_login_required
from users.models import UserActivityCode, User, UserRole
from datetime import datetime
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404


def error_response(api_result, error_message, status_code):
    api_result["result"]["error_message"] = error_message
    return Response(api_result, status=status_code)


@extend_schema(tags=["users"])
class PublisherSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        response = APIResult()
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return error_response(response.api_result, error_message="نام کاربری قبلا ثبت شده است.", status_code=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return error_response(response.api_result, error_message="ایمیل قبلا ثبت شده است.", status_code=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(username=username, email=email, is_publisher=True, is_confirm=False)

            user.set_password(password)

            role_id = UserRole.assign_publisher_role(user.id)

            token = generate_jwt_token(user.id, role_id)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
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

            user = get_object_or_404(User, id=user_id)

            if User.objects.exclude(id=user_id).filter(publications_name=publications_name).exists():
                return error_response(response.api_result, error_message="نام تجاری قبلا ثبت شده است", status_code=status.HTTP_400_BAD_REQUEST)

            if User.objects.exclude(id=user_id).filter(phone_number=phone_number).exists():
                return error_response(response.api_result, error_message="شماره همراه قبلا ثبت شده است", status_code=status.HTTP_400_BAD_REQUEST)

            user.phone_number = phone_number
            user.publications_name = publications_name
            user.card_number = card_number
            user.address = address
            user.save()

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class PublisherImageUploadView(GenericAPIView):
    serializer_class = PublisherImageUploadSerializer

    @publisher_login_required
    def put(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PublisherImageUploadSerializer(data=request.data)
        if serializer.is_valid():

            publications_image = serializer.validated_data['publications_image']
            identity_image = serializer.validated_data['identity_image']

            User.update_publisher_files(user_id, publications_image, identity_image)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class UserSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        response = APIResult()
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return error_response(response.api_result, error_message="نام کاربری قبلا ثبت شده است.", status_code=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return error_response(response.api_result, error_message="ایمیل قبلا ثبت شده است", status_code=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email, username=username, is_publisher=False, is_confirm=False)
            user.set_password(password)

            role_id = UserRole.assign_customer_role(user.id)

            token = generate_jwt_token(user.id, role_id)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        response = APIResult()
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            identifier = serializer.validated_data['email_or_username']
            password = serializer.validated_data['password']

            user = User.objects.filter(username=identifier) | User.objects.filter(email=identifier)

            if not user.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user = user.first()

            if not user.password_valid(password):
                return error_response(response.api_result, error_message="کاربر با این اطلاعات وجود ندارد.", status_code=status.HTTP_400_BAD_REQUEST)

            role_id = UserRole.get_user_role_id(user.id)

            token = generate_jwt_token(user.id, role_id)

            response.api_result['data'] = token

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class SendSignUpEmailView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        response = APIResult()
        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            if User.objects.filter(email=email).exists():
                return error_response(response.api_result, error_message="ایمیل قبلا ثبت شده است.", status_code=status.HTTP_400_BAD_REQUEST)

            user_activity = UserActivityCode.create_user_activity_code(email)

            subject = "فعال سازی حساب کاربری"
            template = "users/email_signup.html"
            send_email_background_task(subject, template, user_activity.activity_code, email)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class VerifyEmailCodeView(GenericAPIView):
    serializer_class = VerifyEmailCodeSerializer

    def post(self, request):
        response = APIResult()
        serializer = VerifyEmailCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']

            if not UserActivityCode.valid_user_activity_code(email, activation_code):
                return error_response(response.api_result, error_message="کد وارد شده نا معتبر است.", status_code=status.HTTP_400_BAD_REQUEST)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class SendPasswordResetCodeView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        response = APIResult()
        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            if not User.objects.filter(email=email).exists():
                return error_response(response.api_result, error_message="ایمیل وجود ندارد.", status_code=status.HTTP_400_BAD_REQUEST)

            user_activity = UserActivityCode.create_user_activity_code(email)

            subject = "بازیابی رمز عبور"
            template = "users/reset_password_email.html"
            send_email_background_task(subject, template, user_activity.activity_code, email)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["users"])
class PasswordResetView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        response = APIResult()
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            password = serializer.validated_data['password']

            latest_code = UserActivityCode.objects.filter(email=email).latest('created_date_time')

            if latest_code is None:
                return error_response(response.api_result, error_message="کد وارد شده نامعتبر است.", status_code=status.HTTP_400_BAD_REQUEST)

            current_datetime = datetime.now()

            if current_datetime > latest_code.expire_date_time:
                return error_response(response.api_result, error_message="به علت تاخیر زیاد دسترسی وجود ندارد. دوباره امتحان کنید", status_code=status.HTTP_400_BAD_REQUEST)

            if latest_code.activity_code != activation_code:
                return error_response(response.api_result, error_message="کد وارد شده نامعتبر است.", status_code=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            user.set_password(password)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
