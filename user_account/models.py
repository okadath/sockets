from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now 
from django.contrib.auth.models import User 

#obsolete?
class License(models.Model):
	name = models.CharField(max_length=149, unique=True)
	pricing = models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
	duration = models.IntegerField()
	release_data = models.DateField(default= now)

	def __str__(self):
		return self.name

#obsolete?
class Code(models.Model):
	code = models.CharField(max_length=149, unique=True)
	validity_begins = models.DateField(default=now)
	validity_expires = models.DateField(default= now)
	license = models.ForeignKey(License, related_name='code_license', on_delete=models.CASCADE, blank=True, null=True,default=1)
	is_event_code = models.BooleanField(default=False)

	def __str__(self):
		return self.code

# hidden model
# class Profile(models.Model):
# 	# country = CountryField(blank=True, null=True)
# 	picture = models.FileField(upload_to='pics/', blank=True, null=True)
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	code = models.ForeignKey(Code, related_name='user_code', on_delete=models.CASCADE,null=True)

# 	def __str__(self):
# 		return self.user.username

# el nucleo del sistema de autenticacion
class User_Code(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  # unique=True)
	code = models.ForeignKey(Code, on_delete=models.CASCADE)#, unique=True)

	def __str__(self):
		return str(self.user.username + '_' + self.code.code)


class LoggedInUser(models.Model):
    # user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='logged_in_user', on_delete=models.CASCADE ) 
    # Session keys are 32 characters long
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.user.username+"-"+str(self.session_key))


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)  
	STATUS_CHOICES = [ 
(0,"Aguascalientes"),
(1,"Baja California"),
(2,"Baja California Sur"),
(3,"Campeche"),
(4,"Chiapas"),
(5,"Chihuahua"),
(6,"Coahuila"),
(7,"Colima"),
(8,"Distrito Federal"),
(9,"Durango"),
(10,"Guanajuato"),
(11,"Guerrero"),
(12,"Hidalgo"),
(13,"Jalisco"),
(14,"Estado de Mexico"),
(15,"Michoacan"),
(16,"Morelos"),
(17,"Nayarit"),
(18,"Nuevo Leon"),
(19,"Oaxaca"),
(20,"Puebla"),
(21,"Queretaro"),
(22,"Quintana Roo"),
(23,"San Luis Potosi"),
(24,"Sinaloa"),
(25,"Sonora"),
(26,"Tabasco"),
(27,"Tamaulipas"),
(28,"Tlaxcala"),
(29,"Veracruz"),
(30,"Yucatan"),
(31,"Zacatecas"),
	] 
	state = models.IntegerField(choices=STATUS_CHOICES, default=0)
	city = models.CharField(max_length=150, blank=True, null=True)
	phone = models.CharField(max_length=150, blank=True, null=True)
	work = models.CharField(max_length=150, blank=True, null=True)

