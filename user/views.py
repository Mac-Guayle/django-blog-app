from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)

        messages.success(request, "Basariyla Kayit Oldunuz")
        return redirect("index")
    else:
        return render(request, "register.html", {"form": form})

def loginUser(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Basariyla Giris Yapildi")
            return redirect("index")
        else:
            messages.info(request, "Kullanici Adi veya Parola Yanlis")
            return render(request, "login.html", {"form": form})
    else:
        return render(request, "login.html", {"form": form})

def logoutUser(request):
    logout(request)
    messages.success(request, "Basariyla Cikis Yaptiniz")
    return redirect("index")