import traceback
from django.db import ProgrammingError, InternalError, IntegrityError
from rest_framework.response import Response
from rest_framework import status
from users.api.api_result import APIResult
import logging
import users.api.exceptions as user_exceptions
import accounts.api.exceptions as account_exceptions
from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    response = APIResult()
    status_code = status.HTTP_400_BAD_REQUEST

    known_exceptions = {
        user_exceptions.UsernameAlreadyExistsError: "نام کاربری قبلا ثبت شده است",
        user_exceptions.EmailAlreadyExistsError: "ایمیل قبلا ثبت شده است",
        user_exceptions.PhoneNumberAlreadyExistsError: "شماره تلفن قبلا ثبت شده است",
        user_exceptions.PublicationsNameAlreadyExistsError: "نام تجاری قبلا ثبت شده است",
        user_exceptions.InvalidUserCredentialsError: "اطلاعات ورودی صحیح نمی باشد",
        user_exceptions.EmailDoesNotExistError: "ایمیل یافت نشد",
        user_exceptions.ExpiredCodeError: "کد منقضی شده است",
        user_exceptions.InvalidCodeError: "کد وارد شده نا معتبر است",
        user_exceptions.InvalidFileFormatError: "فایل نامعتبر",
        NotFound: "یافت نشد",

        account_exceptions.InvalidTokenError: "کاربر عزیز لطفا مجددا لاگین شوید",
        account_exceptions.MissingTokenError: "کاربر عزیز لطفا مجددا لاگین شوید",
        account_exceptions.ExpiredSignatureError: "کاربر عزیز لطفا مجددا لاگین شوید",
        account_exceptions.WrongPasswordError: "رمز وارد شده صحیح نیست",

        account_exceptions.PermissionDeniedError: "کاربر عزیز شما به این بخش دسترسی ندارید",

        user_exceptions.FileUploadFailedError: "خطایی هنگام آپلود فایل در سیستم رخ داد",
        ProgrammingError: "An error occurred while running the cursor",
        IntegrityError: "خطایی در اعتبارسنجی داده‌ها رخ داده است",
        InternalError: "خطایی در پایگاه داده رخ داده است",
    }

    authorization_exceptions = (account_exceptions.InvalidTokenError, account_exceptions.MissingTokenError, account_exceptions.ExpiredSignatureError)

    internal_exceptions = (ProgrammingError, IntegrityError, InternalError, user_exceptions.FileUploadFailedError)

    for exception_type, error_message in known_exceptions.items():
        if isinstance(exc, exception_type):

            if isinstance(exc, internal_exceptions):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            if isinstance(exc, authorization_exceptions):
                status_code = status.HTTP_401_UNAUTHORIZED

            if isinstance(exc, NotFound):
                status_code = status.HTTP_404_NOT_FOUND

            if isinstance(exc, account_exceptions.PermissionDeniedError):
                status_code = status.HTTP_403_FORBIDDEN

            return error_response(response, error_message=error_message,
                                  status_code=status_code)

        traceback.print_exc()

    return error_response(response, error_message="خطایی در سرور رخ داده است",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def error_response(response,error_message, status_code):
    response.api_result['result']['error_message'] = error_message
    return Response(response.api_result, status=status_code)