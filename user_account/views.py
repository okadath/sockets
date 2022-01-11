from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from user_account.forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from events import views as view_events
from user_account.models import Code,User_Code ,Profile
from django.shortcuts import get_list_or_404, get_object_or_404
from user_account.forms import UserForm, UserForm_2
from events.views import  see_event
from django.contrib.auth.decorators import login_required
from django.conf import settings
from events.models import ControlDeploy
# mess_error= "Ya tenemos tu correo registrado. Que gusto tener de vuelta; Te esperamos el 4 de Marzo a las 19:30 hrs.  Para ingresar al evento solo necesitaras tu correo electronico{{mail}}"
# mess_error_incorrecto="Datos incorrectos"
# mess_exito="Tu registro ha sido exitoso <br><br> Te esperamos el 4 de Marzo a las 19:30 hrs. Para ingresar al evento solo necesitaras el correo electronico <br> con el que realizaste el registro"

def home(request):
	return render(request, 'home.html')

def logout_view(request):
	logout(request) 
	return redirect('login')

#no se cual sera tu main page, puse esta por si acaso
def dashboard(request):
	return render(request, 'user_account/dashboard.html')


from user_account.auth_backend import PasswordlessAuthBackend,EmailAuthBackend
from django.contrib.auth.forms import AuthenticationForm

mens='El acceso estará disponible el 20 de abril a las 10:00 hrs'
from datetime import datetime
from django.utils.timezone import utc

from datetime import timedelta
 
def landing(request):
    
    #print(control[0].landing_as_main)
    context={}
    control=ControlDeploy.objects.all()
    context["control"]=control[0]
    if request.user.is_authenticated:
        context["user"]=request.user

    if control[0].landing_as_main==True:
        return render(request, 'spa/app/event/pages/landing.html',context)
    if control[0].landing_as_main==False:
        return render(request, 'spa/app/event/pages/login.html',context)

def register_cumbre(request):
    # print("asd")
    # print(request.POST)
    context = {} 
    control=ControlDeploy.objects.all()
    context["control"]=control[0]
    #if request.user.is_authenticated:
        #aqui tenemos que cambiar el slugroom o usar uno main, que bien este podria ser el main
     #   return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online",'slug_room':"1-Programming"}))
    # dummy control, luego quito los links de las templates
    if control[0].free_page ==True: 
        # print("a")
        return HttpResponseRedirect(reverse('room', kwargs={'slug':control[0].event_in_mainpage.slug,
        'slug_room':control[0].room_in_mainpage.slug}))
    if request.method == 'POST':
        mail=request.POST["email"].lower().replace(" ", "")
        # print(request.method)
        context["mail"]=mail
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            try:
                exists_user = User.objects.get(email=mail)
                mess_error=control[0].mess_error
                context["error_messages"]=mess_error
                context["user_form"]=user_form
                return render(request, 'spa/app/event/pages/register.html',  context)
            except Exception as a:
                user = user_form.save(commit=False)
                user.username=mail
                user.first_name=request.POST["first_name"]
                user.last_name=request.POST["last_name"]
                user.email=mail
                user.set_password(mail)
                user.save()     
                Profile.objects.create(user=user,state=request.POST["state"],city=request.POST["city"],phone=request.POST["phone"],work=request.POST["work"])
                mess_exito=control[0].mess_exito
                context["mensaje"]=mess_exito
                return render(request, 'spa/app/event/pages/register.html',context)
                #login(request, user, "django.contrib.auth.backends.ModelBackend")
                #return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online", 'slug_room':"1-Programming"}))
        else:
            user_form = UserForm()
            mess_error_incorrecto=control[0].mess_error_incorrecto
            context["user_form"] = user_form
            context["error_messages"] = mess_error_incorrecto
            return render(request, 'spa/app/event/pages/register.html',context)
        # return HttpResponseRedirect(reverse('error404'))
    else:
        user_form = UserForm() 
        return render(request, 'spa/app/event/pages/register.html', context)

from events.models import Event_User

# mess_error= "Ya tenemos tu correo registrado. Que gusto tener de vuelta; Te esperamos el 4 de Marzo a las 19:30 hrs.  Para ingresar al evento solo necesitaras tu correo electronico{{mail}}"
# mess_error_incorrecto="Datos incorrectos"
# mess_exito="Tu registro ha sido exitoso <br><br> Te esperamos el 4 de Marzo a las 19:30 hrs. Para ingresar al evento solo necesitaras el correo electronico <br> con el que realizaste el registro"



def login_cumbre(request):
    context = {}
    control=ControlDeploy.objects.all()
    context["control"]=control[0]
    if control[0].free_page ==True: 
        # print("a")
        return HttpResponseRedirect(reverse('room', kwargs={'slug':control[0].event_in_mainpage.slug,
        'slug_room':control[0].room_in_mainpage.slug}))
    if request.user.is_authenticated:
        #aqui tenemos que cambiar el slugroom o usar uno main, que bien este podria ser el main
        Event_User.objects.create(user=request.user,event=control[0].event_in_mainpage)
        if control[0].lobby_as_firstpage==False: 
            return HttpResponseRedirect(reverse('room', kwargs={'slug':control[0].event_in_mainpage.slug,
                'slug_room':control[0].room_in_mainpage.slug}))
        else: 
            return HttpResponseRedirect(reverse('see_event', kwargs={'slug':control[0].event_in_mainpage.slug}))

            # return render(request, 'spa/app/event/pages/landing.html',context)
        # return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online",'slug_room':"1-Programming"}))
# /event/gls-online/
    if request.method == 'POST':
        email = request.POST.get('username').replace(" ", "")
        user = PasswordlessAuthBackend.authenticate(user=email)
        # print(user)
        if user:
            if user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if control[0].lobby_as_firstpage==False: 
                    return HttpResponseRedirect(reverse('room', kwargs={'slug':control[0].event_in_mainpage.slug,
                        'slug_room':control[0].room_in_mainpage.slug}))
                else: 
                    return HttpResponseRedirect(reverse('see_event', kwargs={'slug':control[0].event_in_mainpage.slug}))
                # return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online",'slug_room':"1-Programming"}))
            else:
                mess_inactivo= control[0].mess_inactivo

                context["error_messages"] =mess_inactivo
                return render(request, 'spa/app/event/pages/login.html', context)
        else:
            mess_no_registrado= control[0].mess_no_registrado
            context["mail"]=email
            context["error_messages"] =mess_no_registrado
            return render(request, 'spa/app/event/pages/login.html', context)
    else:
        return render(request, 'spa/app/event/pages/login.html', context)
