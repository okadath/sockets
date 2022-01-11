from rest_framework import serializers
from events.models import *
from rest_framework import permissions
from django.contrib.auth.models import User

# from django.contrib.auth.models import User
# para que serialize los countries como parte de sus elementos
# from django_countries.serializers import CountryFieldMixin
# from django.contrib.auth.models import User
# from media.models import Playlist

class QuestionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='User.username', required=True)
    email = serializers.CharField(source='speakerdosha.user.email', required=True)
    message = serializers.CharField(source='Question.text', required=True)
    class Meta:
        model = Question
        fields = ('email', 'message')
        # fields = '__all__'
    # username = serializers.CharField(source='user.username', required=True)
    # code = serializers.CharField(source='code.code', required=True)

    # class Meta:
    #     model = User_Code
    #     fields = ('id', 'username', 'code')