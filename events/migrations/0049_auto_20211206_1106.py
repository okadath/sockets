# Generated by Django 2.2.13 on 2021-12-06 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0048_auto_20211128_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='controldeploy',
            name='fecha_fin_jsform',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='controldeploy',
            name='fecha_inicio_jsform',
            field=models.TextField(blank=True, help_text='Formulario de JS, formato-> 12/03/2021 05:25 PM ', null=True),
        ),
    ]
