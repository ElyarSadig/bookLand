from decouple import config
import jwt
import datetime


def generate_jwt_token(user_id, role_id):
    secret_key = config('JWT_SECRET_KEY')

    token_payload = {
        "user_id": user_id,
        "role_id": role_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }

    token = jwt.encode(token_payload, secret_key, algorithm="HS256")

    return token


def decode_jwt_token(token, secret_key):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Token is invalid or corrupted.")
        return None
