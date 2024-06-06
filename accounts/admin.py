from django.contrib import admin
from .models import WalletAction, WalletActionType, Discount, UserDiscount


class WalletActionAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'action_type', 'amount', 'is_successful', 'created_date')
    list_filter = ('action_type', 'is_successful', 'created_date')
    search_fields = ('user__username', 'action_type__action_type', 'amount', 'description')

    def user_username(self, obj):
        return obj.user.username

    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def action_type(self, obj):
        return obj.action_type.action_name

    action_type.admin_order_field = 'action_type__action_type'
    action_type.short_description = 'Action Type'


class WalletActionTypeAdmin(admin.ModelAdmin):
    list_display = ('action_type',)
    search_fields = ('action_type',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'quantity', 'percent', 'created_date', 'expire_date', 'is_delete')
    list_filter = ('is_delete', 'created_date', 'expire_date')
    search_fields = ('code', 'quantity', 'percent')


class UserDiscountAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'discount_code')
    search_fields = ('user__username', 'discount__code')

    def user_username(self, obj):
        return obj.user.username

    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'User Username'

    def discount_code(self, obj):
        return obj.discount.code

    discount_code.admin_order_field = 'discount__code'
    discount_code.short_description = 'Discount Code'


admin.site.register(UserDiscount, UserDiscountAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(WalletActionType, WalletActionTypeAdmin)
admin.site.register(WalletAction, WalletActionAdmin)