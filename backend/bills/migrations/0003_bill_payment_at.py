# Generated by Django 3.0.7 on 2020-06-13 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20200613_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='payment_at',
            field=models.DateTimeField(null=True),
        ),
    ]