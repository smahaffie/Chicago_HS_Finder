from django.contrib.auth.models import User
from django.contrib.auth.models import authenticate

def new_user(firstname, lastname, email, password):
    user = User.objects.create_user(firstname, email, password)
    user.last_name = lastname
    user.save()

def change_password(username, newpassword):
    pass