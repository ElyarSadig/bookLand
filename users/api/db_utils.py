from django.db import connection
import hashlib
from .file_handler import process_and_upload_identity_path, process_and_upload_publications_image
from datetime import datetime
from .exceptions import EmailDoesNotExistError, ExpiredCodeError, InvalidCodeError
import os


class UserAuthenticationDBUtils:

    @classmethod
    def get_user_password_from_username_or_email(cls, identifier):
        query = """
            SELECT Id, HashedPassword, Salt FROM public.Users
            WHERE (username = %s OR email = %s)
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [identifier, identifier])
            result = cursor.fetchone()
            if result is None:
                return None, None, None
            return result

    @classmethod
    def password_match(cls, stored_password, password, salt):
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password == stored_password


class UserManagementDBUtils:

    @classmethod
    def create_user(cls, username, email, password, is_publisher=False, is_confirm=False):
        salt = os.urandom(32).hex()
        password_salt = password + salt
        password_hash = hashlib.sha256(password_salt.encode()).hexdigest()
        query = """
            INSERT INTO public.Users (Username, Email, HashedPassword, Salt, IsActive, IsPublisher, IsConfirm, RegistrationDate)
            VALUES (%s, %s, %s, %s , TRUE, %s, %s, NOW() + INTERVAL '3 hours 30 minutes')
            RETURNING Id
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [username, email, password_hash, salt, is_publisher, is_confirm])
            return cursor.fetchone()[0]

    @classmethod
    def publications_name_exists(cls, publications_name):
        query = "SELECT EXISTS (SELECT 1 FROM public.Users WHERE PublicationsName = %s)"

        with connection.cursor() as cursor:
            cursor.execute(query, [publications_name])
            return cursor.fetchone()[0]

    @classmethod
    def email_exists(cls, email):
        query = "SELECT EXISTS (SELECT 1 FROM public.Users WHERE Email = %s)"

        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            return cursor.fetchone()[0]

    @classmethod
    def username_exists(cls, username):
        query = "SELECT EXISTS (SELECT 1 FROM public.Users WHERE Username = %s)"

        with connection.cursor() as cursor:
            cursor.execute(query, [username])
            return cursor.fetchone()[0]

    @classmethod
    def phone_number_exists(cls, phone_number):
        query = "SELECT EXISTS (SELECT 1 FROM public.Users WHERE PhoneNumber = %s)"

        with connection.cursor() as cursor:
            cursor.execute(query, [phone_number])
            return cursor.fetchone()[0]

    @classmethod
    def update_publisher_info(cls, user_id, phone_number, publications_name, card_number, address):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.Users
                SET PhoneNumber = %s,
                    PublicationsName = %s,
                    CardNumber = %s,
                    Address = %s
                WHERE Id = %s
                """,
                [phone_number, publications_name, card_number, address, user_id]
            )

    @classmethod
    def update_publisher_files(cls, user_id, publications_image, identity_image):

        publications_file_path = ""

        if publications_image is not None:
            publications_file_path = process_and_upload_publications_image(publications_image)

        identity_file_path = process_and_upload_identity_path(identity_image)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.Users
                SET IdentityImage = %s,
                    PublicationsImage = %s
                WHERE Id = %s
                """,
                [identity_file_path, publications_file_path, user_id]
            )

    @classmethod
    def update_user_password(cls, password, email):
        salt = os.urandom(32).hex()
        password_salt = password + salt
        new_hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.Users
                SET HashedPassword = %s,
                    Salt = %s
                WHERE email = %s;
                """,
                [new_hashed_password, salt, email]
            )


class UserRoleDBUtils:

    @classmethod
    def get_user_role_id(cls, user_id):
        query = """
            SELECT RoleId FROM public.UserRoles
            WHERE UserId = %s
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            role_data = cursor.fetchone()
            return role_data[0] if role_data else 3

    @classmethod
    def assign_user_role(cls, user_id, role_id):
        query = """
            INSERT INTO public.UserRoles (UserId, RoleId)
            VALUES (%s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, role_id])


class UserActivityDBUtils:

    @classmethod
    def create_user_activity_code(cls, email, activation_code):
        query = """
                INSERT INTO public.UserActivityCodes (Email, ActivationCode, CreatedDateTime, ExpireDateTime)
                VALUES (%s, %s, NOW() + '3 hours 30 minutes', NOW() + '3 hours 32 minutes')
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [email, activation_code])

    @classmethod
    def get_latest_activation_code(cls, email):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT ActivationCode, ExpireDateTime
                FROM public.UserActivityCodes
                WHERE Email = %s
                ORDER BY CreatedDateTime DESC
                LIMIT 1;
                """, [email]
            )

            row = cursor.fetchone()

            return row

    @classmethod
    def validate_activation_code(cls, email, activation_code):
        latest_activation_code = cls.get_latest_activation_code(email)

        if not latest_activation_code:
            raise EmailDoesNotExistError()

        code, expired_datetime = latest_activation_code
        current_datetime = datetime.now()

        if current_datetime > expired_datetime:
            raise ExpiredCodeError()

        if code != activation_code:
            raise InvalidCodeError()
