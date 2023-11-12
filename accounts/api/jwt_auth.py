from functools import wraps
from .exceptions import MissingTokenError, InvalidTokenError, ExpiredSignatureError
import jwt
from decouple import config


def extract_user_and_role_id(token):
    secret_key = config("JWT_SECRET_KEY")
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        role_id = decoded_token.get("role_id")
        return user_id, role_id

    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()

    except jwt.InvalidTokenError:
        raise InvalidTokenError()

    except Exception:
        raise Exception()


def login_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]

            user_id, role_id = extract_user_and_role_id(token)

            return view_func(self, request, user_id, role_id, *args, **kwargs)

        else:
            raise MissingTokenError()

    return wrapper

