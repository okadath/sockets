# Generated by Django 2.2.13 on 2021-11-27 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_nj_encuesta_nj_registro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suvw_encuesta',
            old_name='q1_calificacion_del_lugar',
            new_name='q1_calificacion_de_informacion',
        ),
        migrations.RenameField(
            model_name='suvw_encuesta',
            old_name='q2_calificacion_del_duracion',
            new_name='q2_calificacion_de_valor',
        ),
        migrations.RenameField(
            model_name='suvw_encuesta',
            old_name='q3_calificacion_del_contenido_presentaciones',
            new_name='q3_calificacion_de_duracion',
        ),
        migrations.RemoveField(
            model_name='suvw_encuesta',
            name='q4_calificacion_del_informacion_interaccion',
        ),
        migrations.RemoveField(
            model_name='suvw_encuesta',
            name='q5_calificacion_general',
        ),
        migrations.RemoveField(
            model_name='suvw_encuesta',
            name='q6_comentarios',
        ),
        migrations.AddField(
            model_name='suvw_encuesta',
            name='q4_comentarios',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='q1_calificacion_del_formato',
            field=models.CharField(choices=[('100', '100'), ('90', '90'), ('80', '80'), ('70', '70'), ('60', '60'), ('50', '50'), ('40', '40'), ('30', '30'), ('20', '20'), ('10', '10')], default='50', max_length=3),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='q2_calificacion_de_medidas_sanidad',
            field=models.CharField(choices=[('100', '100'), ('90', '90'), ('80', '80'), ('70', '70'), ('60', '60'), ('50', '50'), ('40', '40'), ('30', '30'), ('20', '20'), ('10', '10')], default='50', max_length=3),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='q3_calificacion_de_duracion',
            field=models.CharField(choices=[('100', '100'), ('90', '90'), ('80', '80'), ('70', '70'), ('60', '60'), ('50', '50'), ('40', '40'), ('30', '30'), ('20', '20'), ('10', '10')], default='50', max_length=3),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='q4_calificacion_de_presentacion_producto',
            field=models.CharField(choices=[('100', '100'), ('90', '90'), ('80', '80'), ('70', '70'), ('60', '60'), ('50', '50'), ('40', '40'), ('30', '30'), ('20', '20'), ('10', '10')], default='50', max_length=3),
        ),
        migrations.AlterField(
            model_name='nj_encuesta',
            name='q5_calificacion_general_experiencia',
            field=models.CharField(choices=[('100', '100'), ('90', '90'), ('80', '80'), ('70', '70'), ('60', '60'), ('50', '50'), ('40', '40'), ('30', '30'), ('20', '20'), ('10', '10')], default='50', max_length=3),
        ),
        migrations.AlterField(
            model_name='nj_registro',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='suvw_carta_responsiva',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='suvw_encuesta',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='suvw_privacidad',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='suvw_privacidad_2',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='textarticle',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]