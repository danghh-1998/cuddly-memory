# Generated by Django 3.0.6 on 2020-06-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bounding_boxes', '0003_auto_20200511_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='boundingbox',
            name='context',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
