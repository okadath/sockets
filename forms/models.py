from django.db import models
from django.utils.timezone import now
from djrichtextfield.models import RichTextField


# Create your models here.
##
# SUVW ENCUESTA
##
class JuntaVP_Encuesta(models.Model):
    CHOICES_CALIFICACION = [
        ('10', '10'),
        ('20', '20'),
        ('30', '30'),
        ('40', '40'),
        ('50', '50'),
        ('60', '60'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100'),
    ]
    CHOICES_DURACION = [
        ("ML", "Muy Larga"),
        ("L", "Larga"),
        ("A", "Adecuada"),
        ("R", "Rápida"),
        ("MR", "Muy Rápida"),
    ]
    q1_calificacion_de_informacion = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q2_calificacion_de_valor = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q3_calificacion_de_duracion = models.CharField(choices=CHOICES_DURACION, default="A",
                                                   max_length=2)
    # q4_calificacion_del_informacion_interaccion = models.CharField(choices=CHOICES_CALIFICACION, default='50',
    #                                                                max_length=3)
    # q5_calificacion_general = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q4_comentarios = models.TextField(null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = 'Resultado de Encuesta - ' + str(self.id)
        return display_string


class SUVW_Privacidad(models.Model):
    nombre = models.CharField(max_length=149)
    apellido = models.CharField(max_length=149)
    acepto_terminos = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = str(self.nombre) + ' ' + str(self.apellido)
        return display_string


class SUVW_Privacidad_2(models.Model):
    nombre = models.CharField(max_length=149)
    apellido = models.CharField(max_length=149)
    acepto_terminos = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = str(self.nombre) + ' ' + str(self.apellido)
        return display_string


class SUVW_Carta_Responsiva(models.Model):
    nombre = models.CharField(max_length=149)
    apellido = models.CharField(max_length=149)
    acepto_terminos = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = str(self.nombre) + ' ' + str(self.apellido)
        return display_string


##
# ARTICULOS Y AVISOS
##
class TextArticle(models.Model):
    titulo = models.CharField(max_length=149)
    key = models.CharField(max_length=149, default='identificador')
    contenido = RichTextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.titulo


##
# ENCUESTA NUEVO JETTAA
##
class NJ_Encuesta(models.Model):
    CHOICES_CALIFICACION = [
        ('100', '100'),
        ('90', '90'),
        ('80', '80'),
        ('70', '70'),
        ('60', '60'),
        ('50', '50'),
        ('40', '40'),
        ('30', '30'),
        ('20', '20'),
        ('10', '10'),
    ]
    q1_calificacion_del_formato = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q2_calificacion_de_medidas_sanidad = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q3_calificacion_de_duracion = models.CharField(choices=CHOICES_CALIFICACION, default='50',
                                                   max_length=3)
    q4_calificacion_de_presentacion_producto = models.CharField(choices=CHOICES_CALIFICACION, default='50',
                                                                max_length=3)
    q5_calificacion_general_experiencia = models.CharField(choices=CHOICES_CALIFICACION, default='50', max_length=3)
    q6_comentarios = models.TextField(null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = 'Resultado de Encuesta - ' + str(self.id)
        return display_string


class NJ_Registro(models.Model):
    nombre = models.CharField(max_length=149)
    apellido = models.CharField(max_length=149)
    acepto_terminos_privacidad = models.BooleanField(default=True)
    acepto_recepcion_giveaway = models.BooleanField(default=True)
    acepto_uso_imagen = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        display_string = str(self.nombre) + ' ' + str(self.apellido)
        return display_string
