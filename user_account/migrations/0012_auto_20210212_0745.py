# Generated by Django 2.2.13 on 2021-02-12 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0011_auto_20210127_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='work',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
