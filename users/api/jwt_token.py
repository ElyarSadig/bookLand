from decouple import config
import jwt
import datetime


def generate_jwt_token(user_id, role_id):
    secret_key = config('JWT_SECRET_KEY')

    token_payload = {
        "user_id": user_id,
        "role_id": role_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    }

    token = jwt.encode(token_payload, secret_key, algorithm="HS256")

    return token