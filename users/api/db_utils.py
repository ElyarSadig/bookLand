from django.db import connection
import hashlib
from .file_handler import process_and_upload_identity_path, process_and_upload_publications_image


class UserAuthenticationDBUtils:

    @classmethod
    def get_user_password_from_username_or_email(cls, identifier):
        query = """
            SELECT Id, HashedPassword FROM public.Users
            WHERE (username = %s OR email = %s)
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [identifier, identifier])
            result = cursor.fetchone()
            if result is None:
                return None, None
            return result

    @classmethod
    def password_match(cls, stored_password, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == stored_password


class UserManagementDBUtils:

    @classmethod
    def create_user(cls, username, email, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
            INSERT INTO public.Users (Username, Email, HashedPassword, IsActive, IsPublisher, IsConfirm, RegistrationDate)
            VALUES (%s, %s, %s, TRUE, FALSE, FALSE, NOW() + INTERVAL '3 hours 30 minutes')
            RETURNING Id
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [username, email, password_hash])
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
    def create_publisher_user(cls, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data['phone_number']
        publications_name = validated_data['publications_name']
        card_number = validated_data['card_number']
        identity_path = validated_data['identity_image']
        publications_image = validated_data['publications_image']
        address = validated_data['address']

        identity_path_uuid = process_and_upload_identity_path(identity_path)
        publications_image_uuid = process_and_upload_publications_image(publications_image)

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        query = """
            INSERT INTO public.Users (Username, Email, HashedPassword, IsActive, IsPublisher, IsConfirm,
            RegistrationDate, PhoneNumber, PublicationsName, CardNumber, IdentityPath, PublicationsImage, Address)
            VALUES (%s, %s, %s, TRUE, TRUE, FALSE, NOW() + INTERVAL '3 hours 30 minutes', %s, %s, %s, %s, %s, %s)
            RETURNING Id
            """

        with connection.cursor() as cursor:
            cursor.execute(query, [username, email, password_hash, phone_number, publications_name,
                                   card_number, identity_path_uuid, publications_image_uuid, address])

            return cursor.fetchone()[0]

    @classmethod
    def update_user_password(cls, password, email):
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
