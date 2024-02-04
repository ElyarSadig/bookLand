from django.db import models
from users.models import User


class WalletActionType(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    action_type = models.CharField(max_length=255, unique=True, db_column='actiontype')

    def __str__(self):
        return self.action_type

    class Meta:
        managed = False
        db_table = 'walletactiontypes'


class WalletAction(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    action_type = models.ForeignKey(WalletActionType, on_delete=models.CASCADE, db_column='actiontypeid')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    amount = models.FloatField(db_column='amount')
    is_successful = models.BooleanField(default=False, db_column='issuccessful')
    description = models.TextField(db_column='description')
    created_date = models.DateTimeField(auto_now_add=True, db_column='createddate')

    def __str__(self):
        return self.user.username + " | " + str(self.amount)

    class Meta:
        managed = False
        db_table = "walletactions"


class Discount(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    code = models.CharField(max_length=255, unique=True, db_column='code')
    quantity = models.IntegerField(db_column='quantity')
    percent = models.FloatField(db_column='percent')
    created_date = models.DateTimeField(auto_now_add=True, db_column='createddate')
    expire_date = models.DateTimeField(db_column='expiredate')
    is_delete = models.BooleanField(db_column='isdelete')

    def __str__(self):
        return self.code + " | " + str(self.quantity)

    class Meta:
        managed = False
        db_table = 'discounts'


class UserDiscount(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, db_column='discountid')

    def __str__(self):
        return self.user.username + " used " + self.discount.code

    class Meta:
        managed = False
        db_table = 'userdiscounts'
