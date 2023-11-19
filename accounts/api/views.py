from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .jwt_auth import login_required
from users.api.api_result import APIResult
from .serializers import PasswordChangeSerializer
from .exceptions import *
from rest_framework.pagination import PageNumberPagination
from .db_utils import AccountManagementDBUtils, hash_password


class ChangePasswordView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    @login_required
    def post(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            stored_password = AccountManagementDBUtils.get_user_stored_password(user_id=user_id)
            hashed_old_password = hash_password(old_password)

            if hashed_old_password == stored_password:

                AccountManagementDBUtils.update_password(new_password=new_password, user_id=user_id)

                return Response(response.api_result, status=status.HTTP_200_OK)

            raise WrongPasswordError()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        username, email = AccountManagementDBUtils.get_username_email(user_id=user_id)

        response.api_result['data'] = {'email': email, 'username': username}
        return Response(response.api_result, status=status.HTTP_200_OK)


class GetUserBookMarksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user_bookmarks = AccountManagementDBUtils.get_user_bookmarks(user_id=user_id)

        response.api_result['data'] = user_bookmarks
        return Response(response.api_result, status=status.HTTP_200_OK)


class GetUserBooksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user_books = AccountManagementDBUtils.get_user_books(user_id=user_id)
        response.api_result['data'] = user_books
        return Response(response.api_result, status=status.HTTP_200_OK)


class GetUserWalletHistoryView(GenericAPIView):
    pagination_class = PageNumberPagination

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        response.api_result['data'] = AccountManagementDBUtils.get_user_wallet_history(self, user_id, request)
        return Response(response.api_result, status=status.HTTP_200_OK)


class DeleteUserBookMarkView(GenericAPIView):

    @login_required
    def delete(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        bookmark_id = kwargs.get('bookmark_id')
        AccountManagementDBUtils.update_user_bookmark(user_id=user_id, bookmark_id=bookmark_id)

        return Response(response.api_result, status=status.HTTP_200_OK)


class UserWalletBalance(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        total_balance = AccountManagementDBUtils.get_total_successful_amount(user_id)

        response.api_result['data'] = total_balance

        return Response(response.api_result, status=status.HTTP_200_OK)

