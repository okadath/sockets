# Generated by Django 2.2.13 on 2021-11-30 19:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0014_auto_20211130_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedinuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
