"""OnlineEXP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from django.conf.urls import url# deprecated django4
from events.views import notes
from user_account.urls import *
# import tinymce
urlpatterns =urlpatterns+ [
path('admin/', admin.site.urls),
path('', include('user_account.urls')),
path('', include('events.urls')),
path('', include('forms.urls')),
# path('summernote/', include('django_summernote.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'JuntaVP'

from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from django.conf.urls import url
# from django.conf.urls import path, include
# from django.urls import path

# para internacionalizar estas paginas debere editar las fucking vistas en django por que si no no comprende el contexto de los idiomas
# ya que usa los nombres por default del auth
# sera algo como lo del code token, pero en web
# https://github.com/django/django/blob/master/django/contrib/auth/views.py

urlpatterns = urlpatterns+[
    re_path(r'^accounts/password/reset/$', PasswordResetView.as_view(template_name='spa/app/event/pages/recovery/password_reset_form.html',html_email_template_name='spa/app/event/pages/recovery/password_reset_email.html'), name='password_reset'),
    re_path(r'^accounts/password/reset/done/$', PasswordResetDoneView.as_view(template_name='spa/app/event/pages/recovery/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='spa/app/event/pages/recovery/password_reset_confirm.html'), name='password_reset_confirm'),
    re_path(r'^accounts/password/reset/complete/$', PasswordResetCompleteView.as_view(template_name='spa/app/event/pages/recovery/password_reset_complete.html'), name='password_reset_complete'),

]