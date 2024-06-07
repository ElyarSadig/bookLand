from django.db import models
from users.api.file_handler import process_and_upload_identity_path, process_and_upload_publications_image
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

PUBLISHER_ROLE_ID = 1
CUSTOMER_ROLE_ID = 2


class User(AbstractUser):
    is_publisher = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    phone_number2 = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    identity_image = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=50, null=True, blank=True)
    publications_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    publications_image = models.CharField(max_length=255, null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    roles = models.ManyToManyField('Role', through='UserRole')
    books = models.ManyToManyField('books.Book', through='books.UserBook', related_name='users_books')
    bookmarks = models.ManyToManyField('books.Book', through='books.UserBookmark', related_name='user_bookmarks')
    discounts = models.ManyToManyField('accounts.Discount', through='accounts.UserDiscount', related_name='users')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @classmethod
    def update_publisher_files(cls, user_id, publications_image, identity_image):
        user = cls.objects.get(pk=user_id)

        if publications_image:
            user.publications_image = process_and_upload_publications_image(publications_image)

        if identity_image:
            user.identity_image = process_and_upload_identity_path(identity_image)

        user.save()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
        ]


class UserActivityCode(models.Model):
    email = models.EmailField(max_length=255)
    activation_code = models.CharField(max_length=6)
    created_date = models.DateTimeField(auto_now_add=True)
    validity_duration = models.DurationField(default=timedelta(minutes=5))

    def __str__(self):
        return f'{self.email} - {self.activation_code}'

    class Meta:
        db_table = 'user_activity_codes'
        indexes = [
            models.Index(fields=['email'], name='user_activity_email_idx'),
            models.Index(fields=['activation_code'], name='activation_code_idx'),
        ]


class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.role

    class Meta:
        db_table = 'roles'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')
        db_table = 'user_roles'

    def __str__(self):
        return f'{self.user.username} - {self.role.role}'

