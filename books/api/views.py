from rest_framework.generics import GenericAPIView
from books.api.db_utils import BookManagementDBUtils
from users.api.api_result import APIResult
from rest_framework.response import Response
from rest_framework import status
from accounts.api.jwt_auth import login_required


class BookDetailView(GenericAPIView):

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()

        data = BookManagementDBUtils.get_book_detail(book_id)

        if len(data) == 0:
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        response.api_result['data'] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


class BookReviewsView(GenericAPIView):

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()

        data = BookManagementDBUtils.get_book_review_counts(book_id)

        if len(data) == 0:
            response.api_result['data'] = [{
                "reviewaverage": 0,
                "reviewcount": 0
            }]
        else:
            response.api_result['data'] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


class BookCategoriesView(GenericAPIView):

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()

        categories = BookManagementDBUtils.get_book_categories(book_id)

        if len(categories) == 0:
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        response.api_result['data'] = [category[0] for category in categories]

        return Response(response.api_result, status=status.HTTP_200_OK)


class OriginalBookFileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        book_id = kwargs.get('book_id')

        if not BookManagementDBUtils.has_user_bought_book(user_id, book_id):
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        original_book_file_path = BookManagementDBUtils.get_original_book_filepath(book_id)

        response.api_result['data'] = original_book_file_path

        return Response(response.api_result, status=status.HTTP_200_OK)