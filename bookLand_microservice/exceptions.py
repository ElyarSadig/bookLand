import traceback
from django.db import ProgrammingError, InternalError, IntegrityError, OperationalError
from rest_framework.response import Response
from rest_framework import status
from users.api.api_result import APIResult
import logging
from users.api.exceptions import *
from accounts.api.exceptions import *


def custom_exception_handler(exc, context):
    response = APIResult()
    status_code = status.HTTP_400_BAD_REQUEST

    known_exceptions = {
        UsernameAlreadyExistsError: "نام کاربری قبلا ثبت شده است",
        EmailAlreadyExistsError: "ایمیل قبلا ثبت شده است",
        PhoneNumberAlreadyExistsError: "شماره تلفن قبلا ثبت شده است",
        PublicationsNameAlreadyExistsError: "ناشر با این قبلا ثبت شده است",
        InvalidUserCredentialsError: "اطلاعات ورودی صحیح نمی باشد",
        EmailDoesNotExistError: "ایمیل یافت نشد",
        ExpiredCodeError: "کد منقضی شده است",
        InvalidCodeError: "کد وارد شده نا معتبر است",
        InvalidFileFormatError: "فایل نامعتبر",

        InvalidTokenError: "توکن نامعتبر",
        MissingTokenError: "توکن وجود ندارد",
        ExpiredSignatureError: "توکن منقضی شده است",

        FileUploadFailedError: "خطایی هنگام آپلود فایل در سیستم رخ داد",
        ProgrammingError: "An error occurred while running the cursor",
        IntegrityError: "خطایی در اعتبارسنجی داده‌ها رخ داده است",
        InternalError: "خطایی در پایگاه داده رخ داده است",
    }

    authorization_exceptions = (InvalidTokenError, MissingTokenError, ExpiredSignatureError)

    internal_exceptions = (ProgrammingError, IntegrityError, InternalError, FileUploadFailedError)

    for exception_type, error_message in known_exceptions.items():
        if isinstance(exc, exception_type):

            if isinstance(exc, internal_exceptions):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            if isinstance(exc, authorization_exceptions):
                status_code = status.HTTP_401_UNAUTHORIZED

            return error_response(response, error_code=exception_type.__name__, error_message=error_message,
                                  status_code=status_code)

        traceback.print_exc()

    return error_response(response, error_code=type(exc).__name__, error_message="خطایی در سرور رخ داده است",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def error_response(response, error_code, error_message, status_code):
    response.api_result['result']['error_code'] = error_code
    response.api_result['result']['error_message'] = error_message
    return Response(response.api_result, status=status_code)