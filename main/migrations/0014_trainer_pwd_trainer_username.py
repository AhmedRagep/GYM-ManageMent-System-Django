# Generated by Django 5.0.1 on 2024-01-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='pwd',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
