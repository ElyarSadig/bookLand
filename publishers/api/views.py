from rest_framework.generics import GenericAPIView
from .serializers import PasswordChangeSerializer, UpdatePublisherProfileSerializer
from .jwt_auth import login_required
from users.api.api_result import APIResult
from accounts.api.exceptions import *
from .db_utils import AccountManagementDBUtils, hash_password
from rest_framework import status
from rest_framework.response import Response


class ChangePasswordView(GenericAPIView):
    serializer_class = PasswordChangeSerializer


    @login_required
    def post(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            stored_password, salt = AccountManagementDBUtils.get_user_stored_password_and_salt(user_id=user_id)

            hashed_old_password = hash_password(old_password, salt)

            if hashed_old_password == stored_password:
                AccountManagementDBUtils.update_password(new_password=new_password, user_id=user_id)

                return Response(response.api_result, status=status.HTTP_200_OK)

            raise WrongPasswordError()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherBooksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        data = AccountManagementDBUtils.get_books_with_sales_info(user_id)

        response.api_result["data"] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


class PublisherProfileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        data = AccountManagementDBUtils.get_publisher_info(user_id)

        response.api_result["data"] = data

        return Response(response.api_result, status=status.HTTP_200_OK)

    @login_required
    def put(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        serializer = UpdatePublisherProfileSerializer(data=request.data)

        if serializer.is_valid():

            address = serializer.validated_data["address"]
            phone_number2 = serializer.validated_data["phone_number2"]
            publications_image = serializer.validated_data["publications_image"]
            card_number = serializer.validated_data['card_number']

            AccountManagementDBUtils.update_publisher_profile(address, phone_number2, publications_image, card_number,
                                                              user_id)

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PublisherWalletHistory(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        data = AccountManagementDBUtils.get_publisher_wallet_history(user_id)

        response.api_result["data"] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


class PublisherWalletBalanceView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        data = AccountManagementDBUtils.get_publisher_wallet_balance(user_id)

        response.api_result["data"] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


