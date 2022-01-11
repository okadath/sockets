from django.urls import path, include 
# from django.conf.urls import url
from events import views
from events import rest_views
# todo lo de aqui es tentativo por que quiza no comprendo bien el enlazamiento de las entidades
urlpatterns = [ 
    path('legal/<slug>/', views.legal, name='legal'),
    path('privacy/<slug>/', views.privacy, name='privacy'),

    path('legal/', views.legal, name='legal'),
    path('privacy/', views.privacy, name='privacy'),

    # path('notes/',views.notes,name='notes'),
    # path('notes/<str:title>',views.edit_note,name='notes'), 
    # path('notes/delete/<str:title>',views.delete_note,name='delete_note'), 


    # path('support/', views.support,name='support'),
    # path('event/',views.all_events,name='all_events'),
    # path('event/<str:name_event>/',views.event,name='event'),
    # path('event/unregistry/<str:name_event>', views.unregistry_event, name='unregistry_event'),
    # path('event/join/<str:name_event>', views.join_event, name='join_event'),

    path('event/<str:slug>/', views.see_event, name='see_event'),
    path('event/<str:slug>/support', views.support, name='support'),
    # indica la subvista a usar, room o notes etc...
    # aqui no funciona el generico, no funciona el chat
    # path('event/<str:name_event>/<str:token>', views.event_nested_views, name='event_ne'),

    path('event/programm/<slug>/', views.Program  , name='Program'), 
    path('event/resources/<slug>/', views.recursos  , name='recursos'), 

    # las url de abajo tiene un valor si devuelve todos y dos valores si devuelve un solo room o anuncio
    # es como el get_object y el get_list, se encesitan las url por el parametro
    path('event/room/<slug>/', views.rooms, name='rooms'),

    # principal
    path('event/room/<slug>/<slug_room>', views.room    , name='room'),

    # no funcionan? creo que  por que no existen anuncios
    # path('event/announcements/<str:name_event>/', views.anuncios  , name='anuncios'),
    # path('event/announcements/<str:name_event>/<str:name_ann>/', views.anuncios  , name='anuncios'), 

    path('event/speaker/<slug>/', views.speaker  , name='speakers'), 
    path('event/speaker/<slug>/<slug_speak>/', views.speaker  , name='speakers'), 

    path('event/notes/<slug>/', views.notes  , name='notes'), 
    path('event/notes/<slug>/<str:title>/',views.edit_note,name='notes'), 
    path('event/notes/<slug>/delete/<str:title>/',views.delete_note,name='delete_note'), 


    # esta vista es necesaria para crear los pdfs aunque nunca se acceda a ella!! no borrar!
    path('notes/pdf/<str:title>', views.create_pdf, name='create_pdf'), 
    path('event/<slug>/user-guide', views.user_guide, name='user_guide'), 
    path('event/sponsors/<slug>/', views.sponsors  , name='sponsors'), 
    path('event/peticiones_oracion/<slug>/', views.supportspiritual  , name='supportspiritual'), 
    path('event/teamedition/<slug>/', views.teamedition  , name='teamedition'),
    path('event/interact/<slug>/', views.wonder_interaction  , name='wonder_interaction'),

    path("POST/send_email",rest_views.SendEmailView.as_view(),name="send_email"),

    path('preguntas/', views.preguntas, name='preguntas'),
    path('getfile/', views.getfile, name='getfile'),


]
