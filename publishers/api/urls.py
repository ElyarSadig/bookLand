from django.urls import path
from .views import ChangePasswordView, PublisherProfileView, PublisherBooksView, PublisherWalletHistory, \
    PublisherWalletBalanceView

urlpatterns = [
    path('change-password', ChangePasswordView.as_view()),
    path('profile', PublisherProfileView.as_view()),
    path('books', PublisherBooksView.as_view()),
    path('wallet-history', PublisherWalletHistory.as_view()),
    path('wallet-balance', PublisherWalletBalanceView.as_view())
]
