# Generated by Django 4.2.6 on 2024-06-05 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='userdiscount',
            index=models.Index(fields=['user', 'discount'], name='user_discount_idx'),
        ),
        migrations.AddIndex(
            model_name='walletaction',
            index=models.Index(fields=['user', 'action_type'], name='user_action_type_idx'),
        ),
    ]
