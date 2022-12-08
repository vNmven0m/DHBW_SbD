from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password


def startpage(request):
    return render(request, "startpage.html")


def settings(request):
    return render(request, "settings.html")
def info(request):
    return render(request, "info.html")

def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "index.html")


def crshare(request):
    return render(request, "crshare.html")


def myshare(request):
    return render(request, "myshare.html")


def shshare(request):
    return render(request, "shshare.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            dj_login(request, user)
            messages.success(request, 'Sie wurden Erfolgreich eingeloggt')
            fname = user.first_name
            lname = user.last_name
            current_user = request.user
            user_id = current_user.id
            print(user_id)
            return render(request, 'index.html', {"fname": fname, "lname": lname})

        else:
            messages.error(request, 'Die eingegebenen Daten sind nicht korrekt')
            return redirect('login')

    return render(request, "login.html")


def signout(request):
    logout(request)
    messages.success(request, "Sie wurden erfolgreich Ausgeloggt")
    return redirect('index')
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        passwordcon = request.POST['passwordcon']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('register')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('register')

        if password != passwordcon:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('register')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        try:
            validate_password(password=password, user=myuser)
        except Exception as e:
            print(e)

        myuser.save()

        messages.success(request, "Dein Account wurde erfolgreich erstellt")
        return redirect('login')

    return render(request, "register.html")


def some_endpoint(request):
    if request.method == 'POST':
        messages.success(request, 'Thanks for using POST')
    else:
        messages.error(request, 'Please use POST on this endpoint.')

    return render(request, 'index.html', {})
