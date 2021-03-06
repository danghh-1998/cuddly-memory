# Generated by Django 3.0.6 on 2020-05-06 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('bounding_boxes', '0001_initial'),
        ('templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boundingbox',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='bounding_boxes', to='templates.Template'),
        ),
    ]
