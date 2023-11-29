from django.urls import path
from books.api.views import BookDetailView


urlpatterns = [
    path('<str:book_id>', BookDetailView.as_view(), name="book-detail")
]