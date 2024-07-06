from rest_framework.generics import GenericAPIView
from users.api.api_result import APIResult
from rest_framework.response import Response
from rest_framework import status
from accounts.api.jwt_auth import login_required
from books.models import Category, Language, UserBook, Book
from books.api.serializers import CategorySerializer, LanguageSerializer, BookDetailSerializer, BookReviewsSerializer


class BookDetailView(GenericAPIView):
    serializer_class = BookDetailSerializer
    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()
        book = Book.objects.filter(id=book_id, is_delete=False).prefetch_related('categories').first()
        if not book:
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)
        serializer = BookDetailSerializer(book)
        response.api_result["data"] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)


class BookReviewsView(GenericAPIView):
    serializer_class = BookReviewsSerializer

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()

        book = Book.objects.filter(id=book_id, is_delete=False).first()

        if not book:
            response.api_result['data'] = None
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(book)
        response.api_result['data'] = serializer.data

        return Response(response.api_result, status=status.HTTP_200_OK)


class BookCategoriesView(GenericAPIView):

    def get(self, request, book_id, *args, **kwargs):
        response = APIResult()
        categories = Category.objects.filter(book_categories__book_id=book_id)
        serializer = CategorySerializer(categories, many=True)
        response.api_result['data'] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)


class OriginalBookFileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        book_id = kwargs.get('book_id')

        book = Book.objects.filter(id=book_id).first()
        if book and book.price == 0:
            book = Book.objects.get(id=book_id)
            response.api_result['data'] = book.original_file
            return Response(response.api_result, status=status.HTTP_200_OK)

        if not UserBook.has_user_bought_book(user_id, book_id):
            return Response(response.api_result, status=status.HTTP_404_NOT_FOUND)

        book = Book.objects.get(id=book_id)
        response.api_result['data'] = book.original_file
        return Response(response.api_result, status=status.HTTP_200_OK)


class CategoriesView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        response = APIResult()
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        response.api_result['data'] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)


class LanguagesView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        response = APIResult()
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        response.api_result['data'] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)