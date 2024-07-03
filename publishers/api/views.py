from rest_framework.generics import GenericAPIView
from .serializers import PasswordChangeSerializer, \
    CreateBookSerializer, BookSerializer, PublisherProfileSerializer, \
    WalletActionSummarySerializer
from .jwt_auth import login_required
from users.api.api_result import APIResult
from rest_framework import status
from rest_framework.response import Response
from books.models import Book
from users.models import User
from django.db.models import Sum, Case, When, IntegerField, Count, F
from django.db.models.functions import Coalesce
from accounts.models import WalletAction
from users.api.file_handler import process_and_upload_book, process_and_upload_book_cover_image


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


class PublisherBooksView(GenericAPIView):
    serializer_class = BookSerializer
    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        publisher_books = Book.objects.filter(publisher_id=user_id).annotate(
            count_of_sold=Coalesce(Count('user_books'), 0),
            income=Coalesce(Sum('user_books__book__price'), 0)
        ).values(
            'id',
            'name',
            'author_name',
            'translator_name',
            'released_date',
            'book_cover_image',
            'price',
            'is_delete',
            'number_of_pages',
            'count_of_sold',
            'income'
        )
        serialized = self.get_serializer(publisher_books, many=True)

        response.api_result["data"] = serialized.data

        return Response(response.api_result, status=status.HTTP_200_OK)

    @login_required
    def post(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        summary = WalletAction.objects.filter(
            user_id=user_id,
            is_successful=True
        ).aggregate(
            deposit=Sum(
                Case(
                    When(action_type_id=1, then='amount'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            withdraw=Sum(
                Case(
                    When(action_type_id=2, then='amount'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        balance = summary["deposit"] - summary["withdraw"]

        if balance < 5000:
            response.api_result["result"]["error_message"] = "ناشر عزیز موجودی حساب شما برای ایجاد کتاب کافی نیست"
            return Response(response.api_result, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                validated_data['book_cover_image'] = process_and_upload_book_cover_image(request.data['book_cover_image'])
                validated_data['demo_file'] = process_and_upload_book(request.data['demo_file'])
                validated_data['original_file'] = process_and_upload_book(request.data['original_file'])
                validated_data["publisher_id"] = user_id
            except:
                response.api_result["result"]["error_message"] = "خطایی در برقراری ارتباط با فایل سرور وجود دارد"
                return Response(response.api_result, status=status.HTTP_424_FAILED_DEPENDENCY)

            serializer.save()

            return Response(response.api_result, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def delete(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()

        book_id = kwargs.get('book_id')
        book = Book.objects.filter(id=book_id, publisher_id=user_id).first()
        if book is not None:
            book.is_delete = True
            book.save()

        return Response(response.api_result, status=status.HTTP_200_OK)


class PublisherProfileView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user = User.objects.get(id=user_id)
        serialized = PublisherProfileSerializer(user)
        response.api_result["data"] = serialized.data
        return Response(response.api_result, status=status.HTTP_200_OK)

    @login_required
    def put(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        user = User.objects.get(id=user_id)

        serializer = PublisherProfileSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if 'address' in validated_data:
                user.address = validated_data['address']
            if 'phone_number2' in validated_data:
                user.phone_number2 = validated_data['phone_number2']
            if 'publications_image' in validated_data:
                user.publications_image = validated_data['publications_image']
            if 'card_number' in validated_data:
                user.card_number = validated_data['card_number']
            user.save()

            return Response(response.api_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherWalletHistory(GenericAPIView):

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

        response.api_result["data"] = wallet_actions

        return Response(response.api_result, status=status.HTTP_200_OK)


class PublisherWalletBalanceView(GenericAPIView):

    @login_required
    def get(self, request, user_id, role_id, *args, **kwargs):
        response = APIResult()
        summary = WalletAction.objects.filter(
            user_id=user_id,
            is_successful=True
        ).aggregate(
            deposit=Sum(
                Case(
                    When(action_type_id=1, then='amount'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            withdraw=Sum(
                Case(
                    When(action_type_id=2, then='amount'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

        serializer = WalletActionSummarySerializer(summary)
        response.api_result["data"] = serializer.data

        return Response(response.api_result, status=status.HTTP_200_OK)


