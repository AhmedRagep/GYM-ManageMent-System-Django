# Generated by Django 5.0.1 on 2024-01-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_subplan_validity_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
