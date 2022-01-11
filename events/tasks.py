from Porsche.celery import app
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@app.task
def enviar_mail(asunto, contenido, destinatario,img=""):
	# send_mail(asunto, contenido, 'noreply@mail.com', [destinatario], fail_silently=False)

	msg = EmailMessage(asunto, contenido, settings.EMAIL_HOST_USER,destinatario )
	msg.content_subtype = "html"
	if img!="":
		msg.attach_file(settings.BASE_DIR+"/"+img)
	msg.send()