# Generated by Django 5.0.1 on 2024-01-12 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='img',
            field=models.ImageField(null=True, upload_to='service/'),
        ),
    ]
