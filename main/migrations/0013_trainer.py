# Generated by Django 5.0.1 on 2024-01-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_subscriber_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('detail', models.TextField()),
                ('img', models.ImageField(upload_to='trainers/')),
            ],
        ),
    ]
