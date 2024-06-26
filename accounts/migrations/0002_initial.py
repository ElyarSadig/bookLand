# Generated by Django 4.2.6 on 2024-06-06 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='walletaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userdiscount',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.discount'),
        ),
        migrations.AddField(
            model_name='userdiscount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='walletaction',
            index=models.Index(fields=['user', 'action_type'], name='user_action_type_idx'),
        ),
        migrations.AddIndex(
            model_name='userdiscount',
            index=models.Index(fields=['user', 'discount'], name='user_discount_idx'),
        ),
    ]
