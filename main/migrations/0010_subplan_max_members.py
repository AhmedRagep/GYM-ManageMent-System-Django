# Generated by Django 5.0.1 on 2024-01-14 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_subplanfeature_subplan_subplanfeature_subplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='max_members',
            field=models.IntegerField(default=0),
        ),
    ]