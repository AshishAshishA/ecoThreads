# Generated by Django 5.0.4 on 2024-04-25 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoThreads_app', '0002_alter_orders_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecoThreads_app.area'),
        ),
    ]
