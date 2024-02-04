from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255, unique=True, db_column='name')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'categories'


class Language(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=50, unique=True, db_column='name')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'languages'


class Review(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, db_column='bookid', related_name='book')
    rating = models.IntegerField(db_column='rating', validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ])
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdat')

    def __str__(self):
        return self.user.username + " reviewed " + self.book.name

    class Meta:
        managed = False
        db_table = 'reviews'


class Book(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    name = models.CharField(max_length=255, db_column='bookname')
    author_name = models.CharField(max_length=255, db_column='authorname')
    translator_name = models.CharField(max_length=255, db_column='translatorname', blank=True, null=True)
    released_date = models.IntegerField(db_column='releaseddate')
    book_cover_image = models.CharField(db_column='bookcoverimage')
    price = models.FloatField(db_column='price')
    description = models.TextField(db_column='description')
    number_of_pages = models.IntegerField(db_column='numberofpages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column='languageid')
    is_delete = models.BooleanField(default=False, db_column='isdelete')
    created_date = models.DateTimeField(db_column='createddatetime', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'books'


class BookCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='categoryid')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookid')
    is_delete = models.BooleanField(default=False, db_column='isdelete')

    def __str__(self):
        return self.category.name

    class Meta:
        managed = False
        db_table = 'bookcategories'


class BookFile(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookid')
    demo_file = models.TextField(db_column='bookdemofile')
    original_file = models.TextField(db_column='bookoriginalfile')

    def __str__(self):
        return self.book.name

    class Meta:
        managed = False
        db_table = "bookfiles"


class Comment(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bookid')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    description = models.TextField(db_column='comment')
    is_delete = models.BooleanField(default=False, db_column='isdelete')
    created_date = models.DateTimeField(auto_now_add=True, db_column='createddate')

    def __str__(self):
        return self.user.username + " commented " + self.book.name

    class Meta:
        managed = False
        db_table = 'comments'


class UserBook(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column="bookid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userid")
    bought_time = models.DateTimeField(auto_created=True, db_column="boughttime")

    class Meta:
        managed = False
        db_table = 'userbooks'


class UserBookmark(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, db_column="bookid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userid")
    added_time = models.DateTimeField(auto_now=True, db_column="addedtime")
    is_delete = models.BooleanField(default=False, db_column="isdelete")

    class Meta:
        managed = False
        db_table = 'userbookmarks'
        unique_together = ('user', 'book')