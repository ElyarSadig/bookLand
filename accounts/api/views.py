from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .jwt_auth import login_required
from users.api.api_result import APIResult
from .serializers import PasswordChangeSerializer, UserProfileSerializer
from rest_framework.pagination import PageNumberPagination
from users.models import User
from accounts.api.serializers import UserBookSerializer, UserBookmarkSerializer
from books.models import Book, UserBookmark
from django.db.models import Q, F, Sum, Case, When, Value, IntegerField
from accounts.models import WalletAction
from .pagination import WalletActionPagination


class ChangePasswordView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    @login_required
    def post(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            user = User.objects.get(id=user_id)
            if not user.check_password(old_password):
                response.api_result["result"]["error_message"] = "رمز عبور قبلی اشتباه است"
                return Response(response.api_result, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        response.api_result["data"] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)


class UserBookMarksView(GenericAPIView):
    serializer_class = UserBookmarkSerializer

    @login_required
    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.prefetch_related(
            'bookmarked_books__publisher',
            'bookmarked_books__language'
        ).get(pk=user_id)
        bookmarked_books = user.bookmarked_books.filter(is_delete=False)
        serializer = self.get_serializer(bookmarked_books, many=True)
        response = APIResult()
        response.api_result['data'] = serializer.data
        return Response(response.api_result, status=status.HTTP_200_OK)


class GetUserBooksView(GenericAPIView):
    serializer_class = UserBookSerializer

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user_books = Book.objects.filter(
            users__id=user_id,
            is_delete=False
        ).select_related(
            'publisher', 'language'
        )
        serializer = self.get_serializer(user_books, many=True)
        response.api_result['data'] = serializer.data

        return Response(response.api_result, status=status.HTTP_200_OK)


class DeleteUserBookMarkView(GenericAPIView):

    @login_required
    def delete(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        book_id = kwargs.get('book_id')
        user_bookmark = UserBookmark.objects.filter(
            Q(user_id=user_id) & Q(book_id=book_id)
        )
        user_bookmark.delete()
        return Response(response.api_result, status=status.HTTP_200_OK)


class GetUserWalletHistoryView(GenericAPIView):
    pagination_class = PageNumberPagination

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        wallet_actions = WalletAction.objects.filter(
            user_id=user_id,
            is_successful=True
        ).select_related('action_type').annotate(
            actiontype=F('action_type__action_type')
        ).values(
            'id', 'actiontype', 'amount', 'is_successful', 'description', 'created_date'
        ).order_by('created_date')

        paginator = WalletActionPagination()
        paginated_results = paginator.paginate_queryset(wallet_actions, request)

        data = {
            "page_size": paginator.page_size,
            "page_index": paginator.page.number,
            "count": paginator.page.paginator.num_pages,
            "data": list(paginated_results)
        }

        response.api_result["data"] = data

        return Response(response.api_result, status=status.HTTP_200_OK)


class UserWalletBalance(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        totals = WalletAction.objects.filter(
            user_id=user_id,
            is_successful=True
        ).aggregate(
            total_deposit=Sum(Case(
                When(action_type_id=1, then='amount'),
                default=Value(0),
                output_field=IntegerField()
            )),
            total_withdraw=Sum(Case(
                When(action_type_id=2, then='amount'),
                default=Value(0),
                output_field=IntegerField()
            ))
        )
        total_deposit = totals['total_deposit'] if totals['total_deposit'] is not None else 0.0
        total_withdraw = totals['total_withdraw'] if totals['total_withdraw'] is not None else 0.0

        total_amount = total_deposit - total_withdraw

        response.api_result["data"] = total_amount

        return Response(response.api_result, status=status.HTTP_200_OK)

