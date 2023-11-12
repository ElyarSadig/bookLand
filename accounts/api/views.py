from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .jwt_auth import login_required


class Ping(GenericAPIView):

    @login_required
    # This is how you obtain user_id, role_id and login_required decorator must be used as well
    def get(self, request, user_id, role_id, *args, **kwargs):
        data = {
            "Ping": "You are Authorized Pong!",
            "user_id": user_id,
            "role_id": role_id,
        }
        return Response(data, status=status.HTTP_200_OK)
