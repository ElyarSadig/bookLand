from decouple import config
import jwt
import datetime
from accounts.api.jwt_auth import extract_user_and_role_id
from functools import wraps
from accounts.api.exceptions import MissingTokenError, PermissionDeniedError


def generate_jwt_token(user_id, role_id):
    secret_key = config('JWT_SECRET_KEY')

    token_payload = {
        "user_id": user_id,
        "role_id": role_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    }

    token = jwt.encode(token_payload, secret_key, algorithm="HS256")

    return token


def publisher_login_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]

            user_id, role_id = extract_user_and_role_id(token)

            if role_id != 1:
                raise PermissionDeniedError()

            return view_func(self, request, user_id, role_id, *args, **kwargs)

        else:
            raise MissingTokenError()

    return wrapper


