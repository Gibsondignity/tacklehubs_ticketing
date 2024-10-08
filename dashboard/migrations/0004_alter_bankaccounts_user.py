# Generated by Django 4.2.2 on 2023-08-16 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_bankaccounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccounts',
            name='User',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)s_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
