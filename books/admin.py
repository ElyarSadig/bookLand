from django.contrib import admin
from .models import Book, Category, BookCategory, Language, Review, Comment, UserBookmark, UserBook
from django.utils.translation import gettext_lazy as _
from users.models import User
from django import forms
from django.utils.html import format_html
from users.api.file_handler import process_and_upload_book_cover_image, process_and_upload_book


class PublisherFilter(admin.SimpleListFilter):
    title = _('Publisher')
    parameter_name = 'publisher'

    def lookups(self, request, model_admin):
        publishers = User.objects.filter(is_publisher=True)
        return [(str(publisher.id), publisher.username) for publisher in publishers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(book__publisher__id=self.value())


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'book_title', 'is_delete')
    list_filter = ('is_delete', 'category__name')
    search_fields = ('category__name', 'book__name')

    def category_name(self, obj):
        return obj.category.name

    category_name.admin_order_field = 'category__name'
    category_name.short_description = 'Category Name'

    def book_title(self, obj):
        return obj.book.name

    def has_delete_permission(self, request, obj=None):
        return False

    book_title.admin_order_field = 'book__name'
    book_title.short_description = 'Book Name'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'book_name', 'rating', 'created_at')
    search_fields = ('user__username', 'book__name')
    list_filter = ('rating', 'created_at')

    def user_username(self, obj):
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def book_name(self, obj):
        return obj.book.name


    book_name.admin_order_field = 'book__name'
    book_name.short_description = 'Book Name'


class BookAdminForm(forms.ModelForm):
    category_id = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Category'
    )
    book_cover_image_upload = forms.FileField(required=False,
                                                widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    book_demo_file_upload = forms.FileField(required=False,
                                                widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'}), label='book-demofile')
    book_original_file_upload = forms.FileField(required=False,
                    widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'}), label='book-original-file')

    class Meta:
        model = Book
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class BookAdmin(admin.ModelAdmin):

    list_display = (
    'publisher_username', 'name', 'author_name', 'translator_name', 'released_date', 'book_cover_image_preview',
    'price',
    'language_name', 'number_of_pages', 'is_delete', 'created_date')
    list_filter = ('is_delete', 'language__name', 'released_date',)
    search_fields = ('publisher__username', 'name', 'author_name', 'translator_name', 'language__name')
    readonly_fields = ('created_date', 'book_cover_image_preview', 'book_cover_image')

    fields = (
        'publisher',
        'name',
        'author_name',
        'translator_name',
        'released_date',
        'book_cover_image_upload',
        'book_cover_image_preview',
        'book_demo_file_upload',
        'book_original_file_upload',
        'price',
        'description',
        'number_of_pages',
        'language',
        'category_id',
        'is_delete',
        'created_date',
    )

    form = BookAdminForm

    def publisher_username(self, obj):
        return obj.publisher.username

    publisher_username.admin_order_field = 'publisher__username'
    publisher_username.short_description = 'Publisher Username'

    def language_name(self, obj):
        return obj.language.name

    language_name.admin_order_field = 'language__name'
    language_name.short_description = 'Language Name'

    def book_cover_image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                           obj.book_cover_image) if obj.book_cover_image else ''

    book_cover_image_preview.short_description = 'Book Cover Image Preview'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        category = form.cleaned_data.get('category_id')

        if category:
            category_id = category.id if hasattr(category, 'id') else category
            BookCategory.objects.create(book=obj, category_id=category_id, is_delete=False)

        if form.cleaned_data['book_cover_image_upload']:
            response = process_and_upload_book_cover_image(form.cleaned_data['book_cover_image_upload'])
            if response:
                obj.book_cover_image = response

        # if form.cleaned_data['book_demo_file_upload']:
        #     response = process_and_upload_book(form.cleaned_data['book_demo_file_upload'])
        #     if response:
        #         book_file_instance.demo_file = response
        #
        # if form.cleaned_data['book_original_file_upload']:
        #     response = process_and_upload_book(form.cleaned_data['book_original_file_upload'])
        #     if response:
        #         book_file_instance.original_file = response

        # book_file_instance.save()
        # obj.save()


class BookFileAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'demo_file', 'original_file')
    search_fields = ('book__name',)
    list_filter = (PublisherFilter,)

    def book_name(self, obj):
        return obj.book.name

    book_name.admin_order_field = 'book__name'
    book_name.short_description = 'Book Name'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_name', 'comment', 'created_date', 'is_delete')
    list_filter = (PublisherFilter, 'is_delete')
    search_fields = ('user__username', 'book__name', 'description')

    def book_name(self, obj):
        return obj.book.name


    book_name.admin_order_field = 'book__name'
    book_name.short_description = 'Book Name'


class UserBooksAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user_username', 'bought_time')
    list_filter = ('bought_time',)
    search_fields = ('book__name', 'user__username', 'bought_time')


    def book_title(self, obj):
        return obj.book.name
    book_title.admin_order_field = 'book__name'
    book_title.short_description = 'Book Title'

    def user_username(self, obj):
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def bought_time(self, obj):
        return obj.bought_time.strftime('%Y-%m-%d %H:%M:%S')
    bought_time.admin_order_field = 'bought_time'
    bought_time.short_description = 'Bought Time'


class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user_username', 'added_time')
    list_filter = ('added_time',)
    search_fields = ('book__name', 'user__username', 'added_time')

    def book_title(self, obj):
        return obj.book.name
    book_title.admin_order_field = 'book__name'
    book_title.short_description = 'Book Title'

    def user_username(self, obj):
        return obj.user.username


    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def added_time(self, obj):
        return obj.added_time.strftime('%Y-%m-%d %H:%M:%S')
    added_time.admin_order_field = 'added_time'
    added_time.short_description = 'Added Time'


admin.site.register(UserBookmark, UserBookmarkAdmin)
admin.site.register(UserBook, UserBooksAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Category, CategoryAdmin)


