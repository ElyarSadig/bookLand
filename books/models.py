from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'languages'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " reviewed " + self.book.name

    class Meta:
        db_table = 'reviews'


class Book(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_books')
    name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    translator_name = models.CharField(max_length=255, blank=True, null=True)
    released_date = models.IntegerField()
    book_cover_image = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(null=True)
    number_of_pages = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    demo_file = models.CharField(max_length=255)
    original_file = models.CharField(max_length=255)
    categories = models.ManyToManyField('Category', through='BookCategory', related_name='books')
    users = models.ManyToManyField(User, through='UserBook', related_name='bought_books')
    bookmarks = models.ManyToManyField(User, through='UserBookmark', related_name='bookmarked_books')

    @property
    def review_average(self):
        return self.reviews.aggregate(average=Avg('rating'))['average']

    @property
    def review_count(self):
        return self.reviews.aggregate(count=Count('rating'))['count']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books'


class BookCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book_categories')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_categories')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.category.name

    class Meta:
        db_table = 'book_categories'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    is_delete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " commented " + self.book.name

    class Meta:
        db_table = 'comments'


class UserBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_books')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    bought_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_books'

    @classmethod
    def has_user_bought_book(cls, user_id, book_id):
        return cls.objects.filter(user_id=user_id, book_id=book_id).exists()


class UserBookmark(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookmarks')
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_bookmarks'
        unique_together = ('user', 'book')