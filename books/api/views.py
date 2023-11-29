from rest_framework.generics import GenericAPIView
from books.api.db_utils import BookManagementDBUtils
from users.api.api_result import APIResult
from rest_framework.response import Response
from rest_framework import status


class BookDetailView(GenericAPIView):

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()

        data = BookManagementDBUtils.get_book_detail(book_id)

        if len(data) == 0:
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        response.api_result['data'] = data

        return Response(response.api_result, status=status.HTTP_200_OK)
