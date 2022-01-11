# from django.conf.urls import url
from django.urls import path, include
from user_account import views

urlpatterns = [
    # path('register/',views.register,name='register'),
    # path('register/<str:code>',views.register,name='register'),
    path('',views.landing,name='landing'),
    path('register/',views.register_cumbre,name='register'),
    path('login/',views.login_cumbre,name='login'),
    path('logout/',views.logout_view,name='logout'), 
    path('dashboard/',views.dashboard,name='dashboard'), 
]
# old urls
# path('',views.home,name='home'), 
# path('login_mail/',views.register_user,name='register_user'),
# path('login_code/',views.login_code,name='login_code'),