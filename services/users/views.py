from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
def logout_user(request):
    """View to allow a loged user to logout"""
    logout(request)
    return redirect("login")


def login_page(request):
    """View to allow a registered user to log"""
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides."
    return render(
        request, "users/signin.html", context={"form": form, "message": message}
    )


def signup_page(request):
    """View used to return a signup form and allows a user to register"""
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "users/signup.html", context={"form": form})
