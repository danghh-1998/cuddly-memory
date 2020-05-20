# Generated by Django 3.0.4 on 2020-05-20 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_tokens', '0002_authtoken_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_tokens',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
