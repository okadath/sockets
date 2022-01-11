# from user_account.models import Profile 
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
# requires to define two functions authenticate and get_user
from django.contrib.auth.models import User

class PasswordlessAuthBackend(ModelBackend):  

    def authenticate( user=None):
        try:
            user =  User.objects.get(username=user)
            # print("el del auth es"+str(user))
            return  user
        except User.DoesNotExist:
            return None

        return None


 


from django.contrib.auth import backends

class EmailAuthBackend(backends.ModelBackend):

    def authenticate(username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
