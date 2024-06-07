from django.db import models
from users.models import User


class WalletActionType(models.Model):
    action_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.action_type

    class Meta:
        db_table = 'wallet_action_types'


class WalletAction(models.Model):
    action_type = models.ForeignKey(WalletActionType, on_delete=models.CASCADE, db_index=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=False)
    amount = models.IntegerField()
    is_successful = models.BooleanField(default=False)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " | " + str(self.amount)

    class Meta:
        db_table = "wallet_actions"
        indexes = [
            models.Index(fields=['user', 'action_type'], name='user_action_type_idx'),
        ]


class Discount(models.Model):
    code = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField()
    percent = models.DecimalField(max_digits=4, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField()
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.code + " | " + str(self.quantity)

    class Meta:
        db_table = 'discounts'


class UserDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " used " + self.discount.code

    class Meta:
        db_table = 'user_discounts'
