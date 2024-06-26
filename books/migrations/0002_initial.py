# Generated by Django 4.2.6 on 2024-06-06 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_books', to='books.book'),
        ),
        migrations.AddField(
            model_name='userbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='books.book'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='books.book'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookcategory',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_categories', to='books.book'),
        ),
        migrations.AddField(
            model_name='bookcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_categories', to='books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarked_books', through='books.UserBookmark', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', through='books.BookCategory', to='books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.language'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='users',
            field=models.ManyToManyField(related_name='bought_books', through='books.UserBook', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='userbookmark',
            index=models.Index(fields=['user', 'book'], name='user_bookmark_book_user_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userbookmark',
            unique_together={('user', 'book')},
        ),
        migrations.AddIndex(
            model_name='userbook',
            index=models.Index(fields=['user', 'book'], name='user_book_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['user', 'book'], name='review_user_book_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['book', 'user'], name='comment_book_user_idx'),
        ),
        migrations.AddIndex(
            model_name='bookcategory',
            index=models.Index(fields=['book', 'category'], name='book_category_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['publisher'], name='publisher_book_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['name'], name='name_book_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['author_name'], name='author_name_idx'),
        ),
    ]
