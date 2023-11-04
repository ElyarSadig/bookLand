import hashlib
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import connection
from users.api.serializers import UserSignUpSerializer, LoginSerializer, PublisherSignUpSerializer, \
    SendEmailSerializer, VerifyEmailCodeSerializer, ResetPasswordSerializer
from users.api.validation import validate_username, validate_email
from django.core.mail import EmailMessage
from users.api.utils import generate_random_code
import threading
import jwt
from decouple import config
import datetime


def send_email(subject, body, from_email, recipient_list):
    email = EmailMessage(
        subject=subject,
        from_email=from_email,
        body=body,
        to=recipient_list,
    )
    email.send()


def send_email_background_task(activation_code, email):
    subject = "Email Verification"
    body = f"Here is your activation code {activation_code}"
    from_email = "BookLand@email.com"
    recipient_list = [email]

    email_thread = threading.Thread(target=send_email, args=(subject, body, from_email, recipient_list))
    email_thread.start()


class PublisherSignUpView(GenericAPIView):
    serializer_class = PublisherSignUpSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }
        serializer = PublisherSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['password2']
            phone_number = serializer.validated_data['phone_number']
            publications_name = serializer.validated_data['publications_name']
            card_number = serializer.validated_data['card_number']
            identity_path = serializer.validated_data['identity_image']
            publications_image = serializer.validated_data['publications_image']
            address = serializer.validated_data['address']

            if not validate_username(username):
                data['result']['errorCode'] = "InvalidUsername"
                data['result']['errorMessage'] = "نام کاربری نامعتبر"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if not validate_email(email):
                data['result']['errorCode'] = "InvalidEmail"
                data['result']['errorMessage'] = "ایمیل نامعتبر"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if password != confirm_password:
                data['result']['errorCode'] = "PasswordNotMatch"
                data['result']['errorMessage'] = "پسورد مطابقت ندارند"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE Username = %s", [username])
                username_exists = cursor.fetchone()[0] > 0

                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE Email = %s", [email])
                email_exists = cursor.fetchone()[0] > 0

                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE PhoneNumber = %s", [phone_number])
                phone_number_exists = cursor.fetchone()[0] > 0

                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE PublicationsName = %s", [publications_name])
                publications_name_exists = cursor.fetchone()[0] > 0

                if username_exists:
                    data["result"]["errorCode"] = "UsernameAlreadyExists"
                    data["result"]["errorMessage"] = "نام کاربری ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                if email_exists:
                    data["result"]["errorCode"] = "EmailAlreadyExists"
                    data["result"]["errorMessage"] = "ایمیل ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                if phone_number_exists:
                    data["result"]["errorCode"] = "phoneNumberExists"
                    data["result"]["errorMessage"] = "شماره قبلا ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                if publications_name_exists:
                    data["result"]["errorCode"] = "publicationsNameExists"
                    data["result"]["errorMessage"] = "نام تجاری قبلا ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                password_hash = hashlib.sha256(password.encode()).hexdigest()

                cursor.execute(
                    """
                    INSERT INTO public.Users (Username, Email, HashedPassword, IsActive, IsPublisher, IsConfirm, 
                    RegistrationDate, PhoneNumber, PublicationsName, CardNumber, IdentityPath, PublicationsImage, Address)
                    VALUES (%s, %s, %s, TRUE, TRUE, TRUE, NOW() + '3 hours 30 minutes', %s, %s, %s, %s, %s, %s)
                    RETURNING Id  -- Retrieve the newly inserted user's ID
                    """,
                    [username, email, password_hash, phone_number, publications_image, card_number, identity_path,
                     publications_image, address]
                )

                user_id = cursor.fetchone()[0]  # Get the newly inserted user's ID

                # Insert the user into the UserRoles model
                cursor.execute(
                    """
                    INSERT INTO public.UserRoles (UserId, RoleId)
                    VALUES (%s, 2)
                    """,
                    [user_id]
                )

            connection.close()

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            data["result"]["errors"] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['password2']

            if not validate_username(username):
                data['result']['errorCode'] = "InvalidUsername"
                data['result']['errorMessage'] = "نام کاربری نامعتبر"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if not validate_email(email):
                data['result']['errorCode'] = "InvalidEmail"
                data['result']['errorMessage'] = "ایمیل نامعتبر"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if password != confirm_password:
                data['result']['errorCode'] = "PasswordNotMatch"
                data['result']['errorMessage'] = "پسورد مطابقت ندارند"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE Username = %s", [username])
                username_exists = cursor.fetchone()[0] > 0

                cursor.execute("SELECT COUNT(*) FROM public.Users WHERE Email = %s", [email])
                email_exists = cursor.fetchone()[0] > 0

                if username_exists:
                    data["result"]["errorCode"] = "UsernameAlreadyExists"
                    data["result"]["errorMessage"] = "نام کاربری ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                if email_exists:
                    data["result"]["errorCode"] = "EmailAlreadyExists"
                    data["result"]["errorMessage"] = "ایمیل ثبت شده است"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            password_hash = hashlib.sha256(password.encode()).hexdigest()

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO public.Users (Username, Email, HashedPassword, IsActive, IsPublisher, IsConfirm, RegistrationDate)
                    VALUES (%s, %s, %s, TRUE, FALSE, FALSE, NOW() + '3 hours 30 minutes')
                    RETURNING Id  -- Retrieve the newly inserted user's ID
                    """,
                    [username, email, password_hash]
                )

                user_id = cursor.fetchone()[0]  # Get the newly inserted user's ID

                # Insert the user into the UserRoles model
                cursor.execute(
                    """
                    INSERT INTO public.UserRoles (UserId, RoleId)
                    VALUES (%s, 3)
                    """,
                    [user_id]
                )

            connection.close()

            return Response(data, status=status.HTTP_201_CREATED)

        data['result']['errors'] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
        }
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            identifier = ""
            if 'username' in serializer.validated_data:
                identifier = serializer.validated_data['username']

            elif 'email' in serializer.validated_data:
                identifier = serializer.validated_data['email']

            password = serializer.validated_data['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            query = """
            SELECT * FROM public.Users
            WHERE (username = %s OR email = %s)
            """

            with connection.cursor() as cursor:
                cursor.execute(query, [identifier, identifier])
                user_data = cursor.fetchone()

                if user_data:
                    stored_password = user_data[3]
                    if stored_password == hashed_password:
                        user_id = user_data[0]

                        query = """
                        SELECT RoleId FROM public.UserRoles
                        WHERE UserId = %s
                        """
                        cursor.execute(query, [user_id])

                        role_data = cursor.fetchone()
                        user_role = role_data[0] if role_data else None

                        if user_role is not None:
                            # Retrieve the secret key from environment variables
                            secret_key = config('JWT_SECRET_KEY')

                            # Generate a JWT token
                            token_payload = {
                                "user_id": user_id,
                                "role_id": user_role,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                            }
                            token = jwt.encode(token_payload, secret_key, algorithm="HS256")
                            data["token"] = token

                        else:
                            data["result"]["errorCode"] = "UserRoleNotFound"
                            data["result"]["errorMessage"] = "User's role not found"

                    else:
                        data["result"]["errorCode"] = "InvalidCredentials"
                        data["result"]["errorMessage"] = "Username or password is incorrect"

                else:
                    data["result"]["errorCode"] = "UserNotFound"
                    data["result"]["errorMessage"] = "Username or email not found"

                connection.close()
                return Response(data, status=status.HTTP_200_OK if "token" in data else status.HTTP_400_BAD_REQUEST)

        else:
            data["result"]["errors"] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class SendSignUpEmailView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }

        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            query = """
            SELECT EXISTS (
                SELECT 1 FROM public.Users
                WHERE Email = %s
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(query, [email])
                email_exists = cursor.fetchone()[0]

                if email_exists:
                    data["result"]["errorCode"] = "EmailExists"
                    data["result"]["errorMessage"] = "EmailAlreadyExists"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                activation_code = generate_random_code()

                query = """
                INSERT INTO public.UserActivityCodes (Email, ActivationCode, CreatedDateTime, ExpireDateTime)
                VALUES (%s, %s, NOW() + '3 hours 30 minutes', NOW() + '3 hours 32 minutes')
                """

                cursor.execute(query, [email, activation_code])

            send_email_background_task(activation_code, email)

            return Response(data, status=status.HTTP_200_OK)

        else:
            data["result"]["errors"] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailCodeView(GenericAPIView):
    serializer_class = VerifyEmailCodeSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }

        serializer = VerifyEmailCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT ActivationCode, ExpireDateTime
                    FROM UserActivityCodes
                    WHERE Email = %s
                    ORDER BY CreatedDateTime DESC
                    LIMIT 1;
                    """,
                    [email]
                )
                row = cursor.fetchone()

            if row is not None:
                code, expired_datetime = row
                current_datetime = datetime.now()

                if current_datetime <= expired_datetime:
                    if code == activation_code:
                        return Response(data, status=status.HTTP_200_OK)

                    data["result"]["errorCode"] = "WrongCode"
                    data["result"]["errorMessage"] = "The Code is wrong"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                data["result"]["errorCode"] = "ExpiredCode"
                data["result"]["errorMessage"] = "The Code has expired"

                return Response(data, status=status.HTTP_403_FORBIDDEN)

            data["result"]["errorCode"] = "InvalidEmail"
            data["result"]["errorMessage"] = "No matching email found"

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data["result"]["errors"] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetCodeView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }

        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            query = """
            SELECT EXISTS (
                SELECT 1 FROM public.Users
                WHERE Email = %s
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(query, [email])
                email_exists = cursor.fetchone()[0]

                if not email_exists:
                    data["result"]["errorCode"] = "EmailDoesNotExist"
                    data["result"]["errorMessage"] = "EmailDoesNotExist"
                    return Response(data, status=status.HTTP_403_FORBIDDEN)

                activation_code = generate_random_code()

                query = """
                INSERT INTO public.UserActivityCodes (Email, ActivationCode, CreatedDateTime, ExpireDateTime)
                VALUES (%s, %s, NOW() + '3 hours 30 minutes', NOW() + '3 hours 33 minutes')
                """

                cursor.execute(query, [email, activation_code])

            send_email_background_task(activation_code, email)

            return Response(data, status=status.HTTP_200_OK)

        else:
            data["result"]["errors"] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = {
            "result": {
                "errorCode": "",
                "errorMessage": "",
                "errors": ""
            },
            "data": ""
        }

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['password2']

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT ActivationCode, ExpireDateTime
                    FROM public.UserActivityCodes
                    WHERE Email = %s
                    ORDER BY CreatedDateTime DESC
                    LIMIT 1;
                    """,
                    [email]
                )
                row = cursor.fetchone()

            if row is not None:
                code, expired_datetime = row
                current_datetime = datetime.datetime.now()

                if current_datetime <= expired_datetime:
                    if code == activation_code:

                        if password != confirm_password:
                            data["result"]["errorCode"] = "PasswordNotMatch"
                            data["result"]["errorMessage"] = "passwords do not match!"
                            return Response(data, status=status.HTTP_400_BAD_REQUEST)

                        new_hashed_password = hashlib.sha256(password.encode()).hexdigest()
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """
                                UPDATE public.Users
                                SET HashedPassword = %s
                                WHERE email = %s;
                                """,
                                [new_hashed_password, email]
                            )
                        return Response(data, status=status.HTTP_200_OK)

                    data["result"]["errorCode"] = "WrongCode"
                    data["result"]["errorMessage"] = "Code is wrong"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                data["result"]["errorCode"] = "ExpiredCode"
                data["result"]["errorMessage"] = "The Code has expired"
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            data["result"]["errorCode"] = "InvalidEmail"
            data["result"]["errorMessage"] = "No matching email found"

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data["result"]["errors"] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


