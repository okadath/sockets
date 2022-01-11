# Generated by Django 2.2.13 on 2020-07-30 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_program_programelement'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=149, unique=True)),
                ('date', models.CharField(max_length=149, unique=True)),
                ('time', models.TextField(max_length=249)),
                ('place_in_programme', models.PositiveIntegerField(default=1)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program_element_room', to='events.Room')),
            ],
        ),
        migrations.RenameModel(
            old_name='Program',
            new_name='Programme',
        ),
        migrations.DeleteModel(
            name='ProgramElement',
        ),
    ]
