# Generated by Django 5.1 on 2024-09-01 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_test_spec'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='is_ended',
            field=models.BooleanField(default=False),
        ),
    ]
