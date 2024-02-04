from django.contrib import admin
from .models import User, UserActivityCode, Role, UserRole
from django import forms
import os
import hashlib
from django.utils.html import format_html
from users.api.file_handler import process_and_upload_identity_path, process_and_upload_publications_image


class UserAdminForm(forms.ModelForm):
    publications_image_upload = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))
    identity_image_upload = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        salt = os.urandom(32).hex()

        password_salt = self.cleaned_data['password'] + salt

        new_hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()

        setattr(self.instance, 'salt', salt)

        return new_hashed_password


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_publisher', 'registration_date', 'publications_image_preview')
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'email', 'password', 'salt', 'is_active', 'registration_date'),
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'phone_number2', 'address'),
        }),
        ('Publisher Information', {
            'fields': ('is_publisher', 'publications_name', 'publications_image_upload', 'publications_image_preview', 'card_number',
                                   'identity_image_upload', 'identity_image_preview'),
        }),
        ('Confirmation', {
            'fields': ('is_confirm',),
        }),
    )
    readonly_fields = ('identity_image_preview', 'publications_image_preview', 'registration_date', 'salt')

    form = UserAdminForm

    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_publisher', 'is_confirm', 'registration_date']


    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

        is_publisher_changed = 'is_publisher' in form.changed_data

        if obj.is_publisher and (is_publisher_changed or not change):
            publisher_role, created = Role.objects.get_or_create(role='Publisher')
            user_role, created = UserRole.objects.get_or_create(user=obj, role=publisher_role)
        elif not obj.is_publisher and (is_publisher_changed or not change):

            customer_role, created = Role.objects.get_or_create(role='Customer')
            user_role, created = UserRole.objects.get_or_create(user=obj, role=customer_role)

        if form.cleaned_data['publications_image_upload']:
            response_publications = process_and_upload_publications_image(form.cleaned_data['publications_image_upload'])
            if response_publications:
                obj.publications_image = response_publications

        if form.cleaned_data['identity_image_upload']:
            response_identity = process_and_upload_identity_path(form.cleaned_data['identity_image_upload'])
            if response_identity:
                obj.identity_image = response_identity

        obj.save()

    def publications_image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.publications_image) if obj.publications_image else ''
    publications_image_preview.short_description = 'Publications Image Preview'

    def identity_image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.identity_image) if obj.identity_image else ''
    identity_image_preview.short_description = 'Identity Image Preview'


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'role_role')
    list_filter = ('role__role',)
    search_fields = ('user__username',)

    def user_username(self, obj):
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def role_role(self, obj):
        return obj.role.role
    role_role.admin_order_field = 'role__role'
    role_role.short_description = 'Role Role'

    def has_delete_permission(self, request, obj=None):
        return False


class RoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'description')
    search_fields = ('role', 'description')




class UserActivityCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'activity_code', 'created_date_time', 'expire_date_time')
    search_fields = ('email', 'activity_code')
    list_filter = ('created_date_time', 'expire_date_time')

    def email(self, obj):
        return obj.email
    email.admin_order_field = 'email'
    email.short_description = 'Email'

    def created_date_time(self, obj):
        return obj.created_date_time
    created_date_time.admin_order_field = 'created_date_time'
    created_date_time.short_description = 'Created Date Time'

    def expire_date_time(self, obj):
        return obj.expire_date_time
    expire_date_time.admin_order_field = 'expire_date_time'
    expire_date_time.short_description = 'Expire Date Time'


admin.site.register(UserActivityCode, UserActivityCodeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(User, UserAdmin)