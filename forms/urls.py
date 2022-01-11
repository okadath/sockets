from django.urls import path
from .views import suvm_landing, SUVM_PrivacidadCreateView, SUVM_Privacidad2CreateView, \
    SUVM_ResponsivaCreateView, NJ_RegistroCreateView, JuntaVP_EncuestaCreateView, nj_landing, nj_avisos, juntavp_success

urlpatterns = [
    # path('encuesta/', SUVM_EncuestaCreateView.as_view(), name='encuesta'),
    # path('privacidadyusodeimagen/', SUVM_PrivacidadCreateView.as_view(), name='privacidad'),
    # path('privacidad/', SUVM_Privacidad2CreateView.as_view(), name='privacidad-2'),
    # path('responsiva/', SUVM_ResponsivaCreateView.as_view(), name='responsiva'),
    # path('', suvm_landing, name='suvw-landing'),path('', suvm_landing, name='landing'),
    path('encuesta/', JuntaVP_EncuestaCreateView.as_view(), name='encuesta'),
    path('registro/', NJ_RegistroCreateView.as_view(), name='registro'),
    path('avisos/', nj_avisos, name='avisos'),
    path('gracias/', juntavp_success, name='gracias'),
    path('', nj_landing, name='suvw-landing'), path('', suvm_landing, name='landing'),
]
