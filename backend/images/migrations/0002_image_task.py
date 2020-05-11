# Generated by Django 3.0.6 on 2020-05-11 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images',
                                    to='tasks.Task'),
        ),
    ]
