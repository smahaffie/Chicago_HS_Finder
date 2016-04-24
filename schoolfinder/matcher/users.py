from django.contrib.auth.models import User
from django.contrib.auth.models import authenticate, login

#authenticate takes username, pass
#login takes user, request

def new_user(firstname, lastname, email, password):
    user = User.objects.create_user(firstname, email, password)
    user.last_name = lastname
    user.save()

def change_password(username, oldpassword, newpassword):
    user = authenticate(username, oldpassword)
    if user is not None:
        u = User.objects.get(username)
        u.set_password(newpassword)
        u.save()
    else:
        print("Incorrect info provided")
        

    
