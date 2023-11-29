from django.urls import path
from .views import ChangePasswordView, UserProfileView, GetUserBooksView, \
    UserBookMarksView, GetUserWalletHistoryView, DeleteUserBookMarkView, UserWalletBalance

urlpatterns = [
    path("change-password", ChangePasswordView.as_view(), name='change-old-password'),
    path("profile", UserProfileView.as_view(), name='user-profile'),
    path("books", GetUserBooksView.as_view(), name='user-books'),

    path("bookmarks", UserBookMarksView.as_view(), name='user-bookmarks'),
    path("bookmarks/<str:book_id>", DeleteUserBookMarkView.as_view(), name='delete-user-bookmark'),

    path("wallet-history", GetUserWalletHistoryView.as_view(), name='user-wallet-history'),
    path("wallet-balance", UserWalletBalance.as_view(), name='user-wallet-balance'),
]
