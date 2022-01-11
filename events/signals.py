import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_account.models import *
from events.models import *

@receiver(post_save, sender=Question)
def create_question(sender, instance, created, **kwargs):
	print(instance)
	if created:
		print(instance.text)
		channel_layer = channels.layers.get_channel_layer()
		async_to_sync(channel_layer.group_send)('chat_default_preguntas', {
			'type': 'chat_message', 
			"message":instance.text
			})