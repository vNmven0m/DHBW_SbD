from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login


def startpage(request):
    return render(request, "startpage.html")


def home(request):
    return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            dj_login(request, user)
            return render(request, "startpage.html")

        else:
            messages.error(request, "Die eingegebenen Daten sind nicht korrekt")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    logout(request)
    messages.success(request, "Sie wurden Ausgeloggt")
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

        myuser = User.objects.create_user(username, email, password)
        myuser.fist_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, "Dein Account wurde erfolgreich erstellt")
        return redirect('login')

    return render(request, "register.html")
