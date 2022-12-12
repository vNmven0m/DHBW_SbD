from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import django.core.files.storage as Storage
from Gesundheitsakte.models import Document
from Gesundheitsakte.models import share


import uuid


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


def permission(request):
    if request.method == 'GET':
        if "id" in request.GET:
            id = request.GET.get('id')
            document = Document.objects.filter(id=id)[0]
            return render(request, "permission.html", {"document": document})

    if request.method == 'POST':
        if "add" in request.POST:
            if "email" in request.POST:
                #user = User.objects.filter(email=request.POST['email'])[0]
                #shr=share.objects.filter(username=request.POST['email'])[0]
                shr = share.objects.create(id=request.GET.get('id'),share_id= int(str(bin(uuid.uuid4().int)).split('b')[1][0:63:1], base=2) ,username=request.POST['email'])
                document = Document.objects.filter(id=request.GET.get('id'))[0]
                document.shared.add(shr)

                return render(request, "permission.html", {"document": document})


        if "delete" in request.POST:
            if "email" in request.POST:
                User.objects.filter(email=request.POST['email'])





def crshare(request):
    if request.method == 'POST':

        try:
            filename = request.POST['docname']
            uploadfile = request.FILES['document']
            filetypes = ['pdf','jpeg','png','jpg','docx']
            if str(uploadfile).rsplit('.', 1)[1] in filetypes:
                location = 'media/' + str(request.user.id) + "/"
                fs = FileSystemStorage(location=location)
                fs.save(filename + '.' + str(uploadfile).rsplit('.', 1)[1], uploadfile)
                while True:
                    try:
                        Document.objects.create(id=int(str(bin(uuid.uuid4().int)).split('b')[1][0:63:1], base=2),
                                                name=filename + '.' + str(uploadfile).rsplit('.', 1)[1], path=location,
                                                owner=request.user)
                    except:
                        continue
                    break
        except Exception as e:
            print(e)
    return render(request, 'crshare.html')


def myshare(request):
    documents = Document.objects.filter(owner=request.user)
    fname = User.first_name
    lname = User.last_name
    if request.method == 'POST':
        if "delete" in request.POST:
            id = request.POST['id']
            document = Document.objects.filter(id=id)[0]
            try:
                for share in document.shared.all():
                    print(share)
                    share.delete()
            except:
                print()
            name = document.name
            document.delete()
            location = 'media/' + str(request.user.id) + "/"
            fs = FileSystemStorage(location=location)
            fs.delete(name)

    return render(request, "myshare.html", {"documents": documents, "fname": fname, "lname": lname})



def shshare(request):
    user = User.objects.filter(id=request.user.id)[0]
    shr = share.objects.filter(username=user.email)[0]
    documents = Document.objects.filter(shared__share_id=shr.share_id)
    print(documents)
    return render(request, "shshare.html", {"documents": documents})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if len(password) < 10:
            messages.error(request, 'Das Passowrt muss aus mindestens 10 Zeichen bestehen')
            return redirect('login')
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
