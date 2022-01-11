from django.shortcuts import render
from django.views.generic import CreateView
from .models import JuntaVP_Encuesta, SUVW_Privacidad, SUVW_Privacidad_2, SUVW_Carta_Responsiva, TextArticle
from .models import NJ_Registro, NJ_Encuesta
from .forms import EncuestaForm, PrivacidadForm, Privacidad2Form, ResponsivaForm


# Create your views here.
def juntavp_success(request):
    return render(request, 'spa/app/event/dashboard/success.html')
##
# SUVW VIEWS
##
def suvm_landing(request):
    return render(request, 'spa/forms/suvw/landing.html')


class JuntaVP_EncuestaCreateView(CreateView):
    model = JuntaVP_Encuesta
    fields = (
        'q1_calificacion_de_informacion',
        'q2_calificacion_de_valor',
        'q3_calificacion_de_duracion',
        'q4_comentarios',
    )
    form = EncuestaForm
    template_name = 'spa/app/event/dashboard/encuesta.html'
    success_url = '../gracias/'


class SUVM_PrivacidadCreateView(CreateView):
    model = SUVW_Privacidad
    fields = (
        'nombre',
        'apellido',
        'acepto_terminos',
    )
    form = PrivacidadForm
    template_name = 'spa/forms/suvw/privacidad.html'
    success_url = '../'

    def get_context_data(self, **kwargs):
        et = super(SUVM_PrivacidadCreateView, self).get_context_data(**kwargs)
        et['article'] = TextArticle.objects.get(key="privacidad")
        return et


class SUVM_Privacidad2CreateView(CreateView):
    model = SUVW_Privacidad_2
    fields = (
        'nombre',
        'apellido',
        'acepto_terminos',
    )
    form = PrivacidadForm
    template_name = 'spa/forms/suvw/privacidad_2.html'
    success_url = '../'

    def get_context_data(self, **kwargs):
        et = super(SUVM_Privacidad2CreateView, self).get_context_data(**kwargs)
        et['article'] = TextArticle.objects.get(key="privacidad2")
        return et


class SUVM_ResponsivaCreateView(CreateView):
    model = SUVW_Carta_Responsiva
    fields = (
        'nombre',
        'apellido',
        'acepto_terminos',
    )
    form = PrivacidadForm
    template_name = 'spa/forms/suvw/responsiva.html'
    success_url = '../'

    def get_context_data(self, **kwargs):
        et = super(SUVM_ResponsivaCreateView, self).get_context_data(**kwargs)
        et['article'] = TextArticle.objects.get(key="responsiva")
        return et


##
# Nuevo Jetta Views
##
def nj_landing(request):
    return render(request, 'spa/forms/nuevo-jetta/landing.html')


class NJ_EncuestaCreateView(CreateView):
    model = NJ_Encuesta
    fields = (
        'q1_calificacion_del_formato',
        'q2_calificacion_de_medidas_sanidad',
        'q3_calificacion_de_duracion',
        'q4_calificacion_de_presentacion_producto',
        'q5_calificacion_general_experiencia',
        'q6_comentarios',
    )
    form = EncuestaForm
    template_name = 'spa/forms/nuevo-jetta/encuesta.html'
    success_url = '../'


class NJ_RegistroCreateView(CreateView):
    model = NJ_Registro
    fields = (
        'nombre',
        'apellido',
        'acepto_uso_imagen',
        'acepto_terminos_privacidad',
        'acepto_recepcion_giveaway',
    )
    form = PrivacidadForm
    template_name = 'spa/forms/nuevo-jetta/registro.html'
    success_url = '../'

    def get_context_data(self, **kwargs):
        et = super(NJ_RegistroCreateView, self).get_context_data(**kwargs)
        et['article'] = TextArticle.objects.get(key="nj-avisos")
        return et


def nj_avisos(request):
    article = TextArticle.objects.get(key="nj-avisos")
    return render(request, 'spa/forms/nuevo-jetta/avisos.html', {'article': article})
