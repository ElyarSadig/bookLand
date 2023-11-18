from django.urls import path
from .views import ChangePasswordView, UserProfileView, GetUserBooksView, \
    GetUserBookMarksView, GetUserWalletHistoryView, DeleteUserBookMarkView

urlpatterns = [
    path("change-password", ChangePasswordView.as_view(), name='change-old-password'),
    path("profile", UserProfileView.as_view()),
    path("books", GetUserBooksView.as_view()),
    path("bookmarks", GetUserBookMarksView.as_view()),
    path("wallet-history", GetUserWalletHistoryView.as_view()),
    path("bookmarks/<str:bookmark_id>", DeleteUserBookMarkView.as_view()),
]
