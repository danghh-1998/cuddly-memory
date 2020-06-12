# Generated by Django 3.0.7 on 2020-06-12 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('clients', '0002_client_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('order_id', models.CharField(max_length=255)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('signature', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(1, 'PAID'), (0, 'UNPAID')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills',
                                   to='clients.Client')),
            ],
            options={
                'db_table': 'bill',
            },
        ),
    ]