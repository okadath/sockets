from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.http import HttpResponse
from django.utils.timezone import now

from events.models import Note, Event,Event_User,Room,LivePlayer,Chat,Announcement,Video,Resource,Speaker, Programme, ProgrammeElement
from events.models import *
from events.forms import NoteForm#,PostAdminForm
from user_account.models import Code
from django.http import HttpResponseRedirect, HttpResponse


import io
from django.http import FileResponse
# from reportlab.pdfgen import canvas
import weasyprint
from weasyprint import HTML
from django.template.loader import get_template
from django.template import Template
from django.contrib.auth.decorators import login_required

# from django_weasyprint import WeasyTemplateResponseMixin

from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied


def free_or_private(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		control=ControlDeploy.objects.all()
		free_page=control[0].free_page 	
		if not free_page:  # if not coach redirect to home page
			if request.user.is_authenticated:
				return func(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse('login', args=(), kwargs={}))
		else:
				return func(request, *args, **kwargs)


	wrapper.__doc__ = func.__doc__
	wrapper.__name__ = func.__name__
	return wrapper



# @login_required(login_url="/")
@free_or_private
def create_pdf(request,title):
	# Create a file-like buffer to receive PDF data.
	# print(request.POST)
	buffer = io.BytesIO()
	try:
		actual_note=get_object_or_404(Note, title=title, user=request.user)
	# si title no existe regresa al main de notas
	except Exception as e: 
		form = NoteForm()
		return HttpResponseRedirect(reverse('notes'))
	b=str(actual_note.text)
	# print(b)
	# a='&lt;p&gt;aaaaaaaaaaaaaaa&lt;/p&gt;'
	# b="<p>aaaaaaaaaaaaaaa</p><br>pa"
	html_template=b.encode()
	pdf_file = weasyprint.HTML(string=html_template).write_pdf(buffer)
	buffer.seek(io.SEEK_SET)
	return FileResponse(buffer, as_attachment=True, filename=title+'.pdf')



from django.shortcuts import get_list_or_404, get_object_or_404

# # lista todos los eventos y los mios para despelgarlos
# # @login_required(login_url="/")
# @free_or_private
# def all_events(request):
# 	ev = Event.objects
# 	try:
# 		my_events=Event_User.objects.filter (user=request.user ) 
# 	except Exception as e:
# 		my_events="" 
# 	return render(request, 'events/all_events.html', {'events': ev, "my_events":my_events} )



# @login_required(login_url="/")
@free_or_private
def support(request, slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag 
	datos_evento = get_object_or_404(Event, slug=slug) 
	chat = Chat.objects.get(event__name="Soporte")
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	context["chat"]=chat
	context["event"]=datos_evento
	context["live"]=live_del_evento
	rooms = Room.objects.all()
	context["rooms"] = rooms
	return render(request, 'spa/app/event/dashboard/support.html', context)

# @login_required(login_url="/")
@free_or_private
def wonder_interaction(request, slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	datos_evento = get_object_or_404(Event, slug=slug)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	context["event"]=datos_evento
	context["live"]=live_del_evento
	return render(request, 'spa/app/event/dashboard/wonder-interaction.html', context)


#este es el lobby inicial, sin haber dado click a las paginas laterales, no hay token que indique a donde ir
# @login_required(login_url="/")
@free_or_private
def see_event(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	context["slug"]=control[0].room_in_mainpage
	datos_evento=get_object_or_404(Event, slug=slug)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.get(event=datos_evento)
	date_now = now()
	lobby_message = 'Bienvenido a NAVIDAD NATURA'
	programme = Programme.objects.get(event=datos_evento)
	programme_elements = ProgrammeElement.objects.filter(programme=programme).order_by('place_in_programme')
	sponsors = Sponsor.objects.all().order_by('?')
	# ==========================emergency query=======================
	# en condiciones normales no deberia haber esto, pero si necesitas llamar a toda la info de todos los modelos de este evento acabo
	# de agregar esta parte para pasarlos directamente por en contexto
	# el precio de usar esto es que deber recargar la pagina para acceder a las notas, desde aqui no hay editor de notas
	# solo puedes leer las ya existentes e imprimirlas

	# rooms_del_evento=Room.objects.filter(event=datos_evento)
	# anunc=Announcement.objects.filter(event=datos_evento)
	# spek=Speaker.objects.filter(event=datos_evento)
	# prog=Video.objects.filter(event=datos_evento)
	# notes=Note.objects.filter(user=request.user)
	# =================================================================
	context["chat"]=chat_event
	context["event"]=datos_evento
	context["live"]=live_del_evento
	context["lobby_message"]=lobby_message
	context["date_now"]=date_now
	context["programme_elements"]=programme_elements
	context["sponsors"]=sponsors
	rooms = Room.objects.all()
	context["rooms"]=rooms
	return render(request, 'spa/app/event/dashboard/lobby.html', context)
	# return render(request, 'spa/app/event/dashboard/lobby.html',
	# 	{"event":datos_evento,"lives":live_del_evento,"chat":chat_event,
	# 	"my_rooms":rooms_del_evento,"announce":anunc,"program":prog,"speakers":spek,'notes': notes, } )


# @login_required(login_url="/")
@free_or_private
def rooms(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	# print("editor")
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"room"} )
	rooms_del_evento=Room.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	# notas_usuario=Note.objects.filter(user=request.user)

# si necesitas pasarle los videos descomenta esto, agregale al render la key "videos":prog, y usa el html de program
	# prog=Video.objects.filter(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)
	context["chat"]=chat_event
	context["event"]=datos_evento
	context["live"]=live_del_evento
	context["token"]="room"
	context["my_rooms"]=rooms_del_evento
	return render(request, 'spa/app/event/dashboard/rooms.html', context)


# # @login_required(login_url="/")
# @free_or_private
@free_or_private
def room(request,slug,slug_room=""):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	print("c")
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="room"
		return render(request, 'events/lobby.html',context)# {"event":datos_evento,"token":"room"} )
	date_now = now()
	room_del_evento=Room.objects.get(slug=slug_room)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	# notes=Note.objects.filter(user=request.user)
	chat_event=Chat.objects.get(event=datos_evento)
	sponsors = Sponsor.objects.all().order_by('?')
	speakerdosha=SpeakerDosha.objects.all()
	# print(speakerdosha)
	context["speakerdosha"]=speakerdosha
	context["date_now"]=date_now
	context["event"]=datos_evento
	context["token"]="room"
	context["my_room"]=room_del_evento
	context["lives"]=live_del_evento
	context["chat"]=chat_event
	context["sponsors"]=sponsors
	rooms = Room.objects.all()
	context["rooms"] = rooms
	# print(notes)
	# if request.method == "POST":
	# 	Note.objects.create(title=str(request.POST["title"]).replace("/", "_"),text=request.POST["text"],user=request.user)
	# 	notes=Note.objects.filter(user=request.user)
	# 	# print('guardado')
	# 	context["notes"]=notes
	# 	return render(request, 'spa/app/event/dashboard/room.html',context)
	# else:
	# 	notes=Note.objects.filter(user=request.user)

	# si necesitas pasarle los videos descomenta esto, agregale al render la key "videos":prog, y usa el html de program
	# prog=Video.objects.filter(event=datos_evento)

	context["notes"]=notes
	return render(request, 'spa/app/event/dashboard/room.html', context)


# @login_required(login_url="/")
@free_or_private
def Program(request,slug ):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="Program"
		return render(request, 'events/lobby.html', context)#, "lives":live_del_evento,"chat":chat_event} )
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)
	prog=Video.objects.filter(event=datos_evento)
	programme = Programme.objects.get(event=datos_evento)
	programme_elements = ProgrammeElement.objects.filter(programme=programme).order_by('place_in_programme')
	live_del_evento=LivePlayer.objects.get(event=datos_evento)

	# print(anunc)
	context["event"]=datos_evento
	context["token"]="Program"
	context["program"]=prog
	context["lives"]=live_del_evento
	context["chat"]=chat_event
	context["programme_elements"]=programme_elements
	context["live"]=live_del_evento
	rooms = Room.objects.all()
	context["rooms"] = rooms

	return render(request, 'spa/app/event/dashboard/schedule.html', context )


# @login_required(login_url="/")
@free_or_private
def recursos(request,slug ):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="recursos"
		return render(request, 'events/lobby.html', context)#, "lives":live_del_evento,"chat":chat_event} )
	chat_event=Chat.objects.filter(event=datos_evento)
	rec=Resource.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	# print(anunc)
	context["event"]=datos_evento
	context["token"]="recursos"
	context["recursos"]=rec
	context["chat"]=chat_event
	context["live"]=live_del_evento
	rooms = Room.objects.all()
	context["rooms"] = rooms
	return render(request, 'spa/app/event/dashboard/resources.html', context)


# @login_required(login_url="/")
@free_or_private
def speaker(request,slug ,slug_speak=""):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="speakers"
		return render(request, 'events/lobby.html', context)#, "lives":live_del_evento,"chat":chat_event} )
	chat_event=Chat.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	if slug_speak=="" :
		spek=Speaker.objects.filter(event=datos_evento)
	else:
		spek=Speaker.objects.filter(slug=slug_speak)
	context["event"]=datos_evento
	context["token"]="speakers"
	context["chat"]=chat_event
	context["live"]=live_del_evento
	context["speakers"]=spek
	rooms = Room.objects.all()
	context["rooms"] = rooms
	return render(request, 'spa/app/event/dashboard/speakers.html', context)


# @login_required(login_url="/")
@free_or_private
def delete_note(request,title,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	notes=Note.objects.filter(user=request.user)
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		return render(request, 'spa/app/event/dashboard/notes.html', context)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)

	try:
		actual_note=get_object_or_404(Note, title=title,user=request.user)
	# si title no existe regresa al main de notas
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		return render(request, 'spa/app/event/dashboard/notes.html', context)
	# print("elimina")
	actual_note.delete()
	return HttpResponseRedirect(reverse('notes', args=[slug]))


# @login_required(login_url="/")
@free_or_private
def edit_note(request,title,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms
	notes=Note.objects.filter(user=request.user)
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		return render(request, 'spa/app/event/dashboard/notes.html',  context)#, "lives":live_del_evento,"chat":chat_event} )
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)
	try:
		actual_note=get_object_or_404(Note, title=title,user=request.user)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		context["lives"]=live_del_evento
		context["chat"]=chat_event

		return render(request, 'spa/app/event/dashboard/notes.html',  context)
	if request.method == "POST":
		# hay un bug si el titulo es espacio vacio. corregir despues
		actual_note.title=str(request.POST["title"]).replace("/", "_")
		actual_note.text=request.POST["text"]
		actual_note.save()
		# queda el nombre antiguo en la url, eso podria causar bugs, tengo que redirigir
		return HttpResponseRedirect(reverse('notes', args=[slug]))

	context["event"]=datos_evento
	context["token"]="notes"
	context["notes"]=notes
	context["lives"]=live_del_evento
	context["chat"]=chat_event
	context["actual"]=actual_note
	return render(request, 'spa/app/event/dashboard/notes.html', context)


from django.contrib.auth.models import User


# @login_required(login_url="/")
@free_or_private
def notes(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms

	notes=Note.objects.filter(user=request.user)
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento=LivePlayer.objects.filter(event=datos_evento)
	except Exception as e:
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		context["live"]=live_del_evento
		return render(request, 'spa/app/event/dashboard/notes.html', context)#, "lives":live_del_evento,"chat":chat_event} )
	live_del_evento = LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)
	us=User.objects.filter(username=request.user)
	# notes=Note.objects.filter(user=request.user)
	# print(request.POST)
	if request.method == "POST":
		Note.objects.create(title=str(request.POST["title"]).replace("/", "_"),text=request.POST["text"],user=request.user)
		notes=Note.objects.filter(user=request.user)
		#print('guardado')
		context["event"]=datos_evento
		context["token"]="notes"
		context["notes"]=notes
		context["live"]=live_del_evento
		context["chat"]=chat_event
		return render(request, 'spa/app/event/dashboard/notes.html', context)
	else:
		notes=Note.objects.filter(user=request.user)

	context["event"]=datos_evento
	context["token"]="notes" 
	context["notes"]=notes
	context["live"]=live_del_evento
	context["chat"]=chat_event
	return render(request, 'spa/app/event/dashboard/notes.html',context)




# @login_required(login_url="/")
@free_or_private
def user_guide(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		print("este evento o slug no existe!!el susario nunca deberia llegar aqui")
		# context["event"] = datos_evento
		# return render(request, 'spa/app/event/dashboard/user-guide.html', {"event":"no hay evento"})
	try:
		# actual_lang = get_object_or_404(Language, lang="English")
		# actual_userguide = get_object_or_404(UserGuideArticle, language=actual_lang)
		# obtiene la primer userguide, si tendran lang descomenta las lineas de arriba
		# y quita la de abajo
		actual_userguide =UserGuideArticle.objects.get(title="Guia de Usuario")
		# print(actual_userguide)
		context["title"] = actual_userguide.title
		a = actual_userguide.content.replace('<', ' ').replace('>', ' ').split()
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["content_string"] = actual_userguide.content
		context["content_url"] = a[3]
		context["event"] = datos_evento
		context["live"] = live_del_evento
		# me falta arreglar y definir esto y su url
		return render(request, 'spa/app/event/dashboard/user-guide.html', context)
	except Exception as e:
		context["event"] = datos_evento
		return render(request, 'spa/app/event/dashboard/user-guide.html', context)


# @login_required(login_url="/")
@free_or_private
def sponsors(request,slug ):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")
		# return render(request,'spa/app/event/dashboard/sponsor.html', {"event":datos_evento,"token":"recursos"})#, "lives":live_del_evento,"chat":chat_event} ) 
	# solo habra un evento, por eso busca todos, si no agregar pk event a Sponsor
	sponsors=Sponsor.objects.all()
	context["event"] = datos_evento
	context["sponsors"] = sponsors
	return render(request, 'spa/app/event/dashboard/sponsor.html', context)


from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
# from events.tasks import enviar_mail
from events.forms import SupportForm


# @login_required(login_url="/")
@free_or_private
# name description image
def supportspiritual(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")

	if request.method == 'POST':
		support_form = SupportForm(data=request.POST)
		if support_form.is_valid():
			supportForm = SupportForm(data=request.POST, files=request.FILES)
			support = support_form.save(commit=False)
			support.user = request.user
			try:
				support.image = request.FILES["image"]
			except Exception as e:
				support.image = ""
			support_form.save()

			texto_mail=request.POST["name"]+'\n'+request.POST["description"]
			asunto='Subject of the Email(Sosporte espiritual)'
			msg = EmailMessage(asunto, texto_mail, "admin@glsteamedition.com", settings.DESTINATARIOS_ORACION)
			msg.content_subtype = "html"
			if support.image!="":
				msg.attach_file(settings.BASE_DIR+"/"+support.image.url)
			msg.send()
			# if support.image=="":
			# 	# enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_ORACION)
			# 	send_mail(asunto, texto_mail, settings.DESTINATARIOS_ORACION)
			# else:
			# 	send_mail(asunto, texto_mail, settings.DESTINATARIOS_ORACION,support.image.url)

			context['form']=support_form
			context['messages']="Mensaje enviado, muchas gracias"
			return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
		else:
			context['form']=support_form
			if request.POST["description"]=="":
				context['error_messages']="La descripcion no debe ir vacia"
				return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
			context['error_messages']="Nombre repetido"
			return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
	else:
		support_form = SupportForm()
		context['form']=support_form
	return render(request, 'spa/app/event/dashboard/spiritualsupport.html', context)


from events.forms import TeamEditionForm


# @login_required(login_url="/")
@free_or_private
# title content image
def teamedition(request,slug):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag
	context["control"]=control[0]
	rooms = Room.objects.all()
	context["rooms"] = rooms
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")

	if request.method == 'POST':
		form = TeamEditionForm(data=request.POST)
		if form.is_valid():
			supportForm = TeamEditionForm(data=request.POST, files=request.FILES)
			support = form.save(commit=False)
			# support.user = request.user
			try:
				support.image = request.FILES["image"]
				file_type = support.image.url.split('.')[-1]
				# print(file_type)
				file_type = file_type.lower()
				if file_type not in settings.IMAGE_FILE_TYPES:
					context['form']=form
					context['error_messages']="El tipo de archivo debe ser jpg,jpeg,png o pdf"
					return render(request, 'spa/app/event/dashboard/teamedition.html',context)
			except Exception as e:
				# raise e
				support.image = ""
			form.save()

			# texto_mail=request.POST["title"]+'\n'+request.POST["content"]
			asunto='Subject of the Email(NEW ONLINE EXP TE)'
			texto_mail=request.POST["title"]+'\n'+request.POST["content"]
			msg = EmailMessage(asunto, texto_mail, "admin@glsteamedition.com", settings.DESTINATARIOS_TE)
			msg.content_subtype = "html" 
			if support.image!="":
				msg.attach_file(settings.BASE_DIR+"/"+support.image.url)
			msg.send()

			# if support.image=="":
			# 	enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_TE)
			# else:
			# 	enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_TE,support.image.url)

			context['form']=form
			context['messages']="Mensaje enviado, muchas gracias"
			return render(request, 'spa/app/event/dashboard/teamedition.html',context)
		else:
			context['form']=form
			#no se como se hace una validacion de no vacio
			if request.POST["content"]=="":
				context['error_messages']="El campo contenido no debe ir vacio"
				return render(request, 'spa/app/event/dashboard/teamedition.html',context)
			context['error_messages']="Nombre repetido"
			return render(request, 'spa/app/event/dashboard/teamedition.html',context)
	else:
		form = TeamEditionForm()
		context['form']=form
	return render(request, 'spa/app/event/dashboard/teamedition.html', context)


def privacy(request,slug=""):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag 
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		context["event"] = datos_evento
	except Exception as e: 
		pass
	priv =UserGuideArticle.objects.get(title="Privacidad")
	context["title"]=priv.title
	context["content_string"]=priv.content
	return render(request,"spa/app/event/pages/privacy.html",context)


def legal(request,slug=""):
	context={}
	control=ControlDeploy.objects.all()
	context["gtag"]=control[0].gtag 
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		context["event"] = datos_evento
	except Exception as e: 
		pass
	legal =UserGuideArticle.objects.get(title="Legal")
	context["title"]=legal.title
	context["content_string"]=legal.content
	return render(request,"spa/app/event/pages/legal.html",context)

def preguntas(request):
	context={}
	questions=Question.objects.all()
	context["questions"]=questions
	return render(request,"spa/app/event/dashboard/preguntas.html",context)
import csv
import io
from django.http import HttpResponse
from django.views.generic import View
import xlsxwriter

def getfile(request):  
	# response = HttpResponse(content_type='text/csv')  
	# response['Content-Disposition'] = 'attachment; filename="questions.csv"'  
	# preguntas = Question.objects.all()  

	# writer = csv.writer(response)  
	# writer.writerow(["speaker","pregunta","usuario"])  

	# for preg in preguntas:  
	#     writer.writerow([preg.speakerdosha,preg.text,preg.user])  
	output = io.BytesIO()

	# Even though the final file will be in memory the module uses temp
	# files during assembly for efficiency. To avoid this on servers that
	# don't allow temp files, for example the Google APP Engine, set the
	# 'in_memory' Workbook() constructor option as shown in the docs.
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()

	# Get some data to write to the spreadsheet.
	preguntas = Question.objects.all() 
	# firstnames = Question.objects.values_list('speakerdosha__name',"text", flat=True)
	# firstnames = list(preguntas)
	# print(firstnames)
	# print(firstnames[0])
	# Write some test data.
	# for row_num, columns in enumerate(data):
	# 	for col_num, cell_data in enumerate(columns):
	# 		worksheet.write(row_num, col_num, cell_data)
	worksheet.write(0, 0, "Speaker")
	worksheet.write(0, 1, "Pregunta")

	for i in range(0,len(preguntas)):
		# for j in range(0,len(firstnames)):
		worksheet.write(i+1, 0, str(preguntas[i].speakerdosha.name))
	for i in range(0,len(preguntas)):
		# for j in range(0,len(firstnames)):
		worksheet.write(i+1, 1, str(preguntas[i].text))
	# for i in range(0,len(preguntas)):
		# worksheet.write(i+1, 2, str(preguntas[i].user.username))


	# Close the workbook before sending the data.
	workbook.close()

	# Rewind the buffer.
	output.seek(0)

	# Set up the Http response.
	filename = 'report.xlsx'
	response = HttpResponse(
		output,
		content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	)
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response  
	# 
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect

# from profiles.models import CoachProfile


# def coach_required(function):
#     def wrapper(request, *args, **kwargs):
#         decorated_view_func = login_required(request)
#         if not decorated_view_func.user.is_authenticated():
#             return decorated_view_func(request)  # return redirect to signin

#         coach = CoachProfile.get_by_email(request.user.email)
#         if not coach:  # if not coach redirect to home page
#             return HttpResponseRedirect(reverse('home', args=(), kwargs={}))
#         else:
#             return function(request, *args, coach=coach, **kwargs)

#     wrapper.__doc__ = function.__doc__
#     wrapper.__name__ = function.__name__
#     return wrapper

#     views.py

# @coach_required
# def view_master_schedule(request, coach):
#     """coach param is passed from decorator"""
#     context = {'schedule': coach.schedule()}
#     return render(request, 'template.html', context)
