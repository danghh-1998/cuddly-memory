# Generated by Django 3.0.4 on 2020-04-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]