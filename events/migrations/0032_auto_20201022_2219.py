# Generated by Django 2.2.13 on 2020-10-22 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0031_auto_20201022_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=149),
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together={('title', 'user')},
        ),
    ]