from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from user_account.models import Profile

# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

# class ProfileForm(forms.ModelForm):
#     # email = forms.EmailField(max_length=200, help_text='Required')    
#     class Meta:
#         model = Profile
        # fields="__all__"
        # fields = ('country', 'picture',"code")#, 'password1', 'password2')

from django import forms
# Deprecated!!!! no se usaran los formularios ante los nuevos cambios
# uno podria eliminar este archivo si fuese necesario
# ya que los formularios se hicieron a mano y ya no manejaremos profile explicitamente
# y los user_codes solo son para login, sin edicion 

# ======================================================
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	# password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ("first_name",'email')
		# fields = ("first_name","last_name",'email','password')

class UserForm_2(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ( 'password',"first_name",'email')

class UserCumbreForm(forms.ModelForm):
	# password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ("first_name","last_name",'email')