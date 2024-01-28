from django.urls import path
from books.api.views import BookDetailView, BookReviewsView, BookCategoriesView, OriginalBookFileView, CategoriesView, \
    LanguagesView


urlpatterns = [
    path('categories', CategoriesView.as_view(), name='book-categories'),
    path('languages', LanguagesView.as_view(), name='book-languages'),
    path('<str:book_id>', BookDetailView.as_view(), name="book-detail"),
    path('<str:book_id>/reviews', BookReviewsView.as_view(), name='book-reviews'),
    path('<str:book_id>/categories', BookCategoriesView.as_view(), name='book-categories'),
    path('originalfilepath/<str:book_id>', OriginalBookFileView.as_view(), name='original-book-file'),
]