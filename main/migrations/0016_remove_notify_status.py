# Generated by Django 5.0.1 on 2024-01-17 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_notify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notify',
            name='status',
        ),
    ]
