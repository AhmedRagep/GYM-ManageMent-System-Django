# Generated by Django 5.0.1 on 2024-02-13 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_trainermsg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainermsg',
            name='user_type',
        ),
    ]
