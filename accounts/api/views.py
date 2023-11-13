from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .jwt_auth import login_required


class ChangePasswordView(GenericAPIView):

    @login_required
    def post(self, request, user_id, role_id, *args, **kwargs):
        pass


class UserProfileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        pass


class SearchUserBooksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        pass


class GetUserBookMarksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        pass


class GetUserBooksView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        pass


class GetUserWalletHistoryView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        pass


class DeleteUserBookMarkView(GenericAPIView):

    @login_required
    def delete(self, request, user_id, role_id, *args, **kwargs):
        bookmark_id = kwargs.get('bookmark_id')
        pass