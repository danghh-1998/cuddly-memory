# Generated by Django 3.0.7 on 2020-06-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bounding_boxes', '0005_auto_20200612_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boundingbox',
            name='recognize_type',
            field=models.SmallIntegerField(
                choices=[(0, 'ENG'), (1, 'VIE'), (2, 'DIGIT'), (3, 'CHECKBOX'), (4, 'EMAIL')], default=0),
        ),
    ]