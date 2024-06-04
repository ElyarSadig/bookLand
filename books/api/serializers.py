from rest_framework import serializers
from books.models import Category, Language, Book
from users.models import User


class BookReviewsSerializer(serializers.ModelSerializer):
    review_average = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['review_average', 'review_count']

    def get_review_average(self, obj):
        return obj.review_average

    def get_review_count(self, obj):
        return obj.review_count


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['publications_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class BookDetailSerializer(serializers.ModelSerializer):
    publisher = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'publisher', 'author_name', 'translator_name', 'demo_file', 'released_date',
                  'book_cover_image', 'price', 'description', 'number_of_pages', 'language',
                  'categories']

    def get_publisher(self, obj):
        return obj.publisher.publications_name

    def get_language(self, obj):
        return obj.language.name

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]