# Generated by Django 5.0.1 on 2024-01-13 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_galleryimage_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubPlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subplan')),
            ],
        ),
    ]
