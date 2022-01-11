from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from events.models import *
from events.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
import bleach
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


class SendEmailView(APIView):
	model=Question
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer 
	permission_classes = [AllowAny]

	# lookup_field = ['user__email', "ID_Freshchat"]
	def post(self, request, *args, **kwargs):
		try:
			user_post=request.data["username"]
			name_post=request.data["name"]
			message_post=request.data["message"]
			if len(name_post)==0:
				return Response ({"message":"Error, debes elegir el nombre y puesto a quien hacer la pregunta"},status=404)
			user_post=bleach.clean(user_post)
			email_post=bleach.clean(name_post)
			message_post=bleach.clean( message_post)
		except Exception as e:
			return Response ({"message":"Error 1, please contact technical support"},status=404)
 

		# print(args)
		# print(kwargs)
		# print(self)
		# print(request.data["email"])
		# try:
		# 	a=Question.objects.get(user__email=email)  
		# 	return Response ({"id":a.name, "email":a.user.email},status=200)
		# except Exception as e:
		try:
			# user=User.objects.get(email=email)
			a=SpeakerDosha.objects.get(name=name_post)
			# print(a)
			user=User.objects.get(username=user_post)
			ques=Question.objects.create(user=user,text=message_post,speakerdosha=a)
		except Exception as e:
			print(e)
			return Response ({"message":"Error 2, please contact technical support"},status=404)
		try:
			texto_mail =  "Pregunta para: " + str(ques.speakerdosha.name) + '\n' + str(message_post) + '\n' + "Pregunta hecha por: " + str(user_post)
			send_mail('Question', texto_mail, settings.EMAIL_HOST_USER, 
				[
					# "gustavo@onel.media",
					"vintaw.01@gmail.com",
					# "norma.guarneros@vw.com.mx",
					# "paulina.acuna@vw.com.mx",
					# "karina.angulo@dosha.com.mx",
					# "karla.guerrero@vw.com.mx",
					# "lucia.ortiz@dosha.com.mx",
					# "carlos.mendoza@dosha.com.mx",
					# "uman.velazquez@dosha.com.mx",
				]
			)
		except Exception as e:
			print(e)
			return Response ({"message":"Error 3, pasarela de gmail, mensaje " +texto_mail+ "correo pasarela"+ settings.EMAIL_HOST_USER },status=404)

		return Response ({"message":" "},status=200)




			# raise e