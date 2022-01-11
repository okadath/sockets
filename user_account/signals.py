from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from user_account.models import LoggedInUser
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
	a=LoggedInUser.objects.filter(user=request.user) 
	if len(a)>=settings.NUM_SESSIONS_ALLOWED:
		b=LoggedInUser.objects.filter(user=request.user).first()
		Session.objects.filter(session_key=b.session_key).delete()
		b.delete()
		stored_session_key =request.session.session_key
		if stored_session_key != None:
			LoggedInUser.objects.get_or_create(user=kwargs.get('user'),session_key=stored_session_key) 
	else:
		if request.session.session_key==None:
			s = SessionStore()
			s.create()
			stored_session_key =s.session_key
		else:
			stored_session_key =request.session.session_key
		LoggedInUser.objects.get_or_create(user=kwargs.get('user'),session_key=stored_session_key) 

@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()