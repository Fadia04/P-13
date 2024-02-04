from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from . import forms


# Create your views here.


def logout_user(request):
    """View to allow a loged in user to logout and return signin page"""
    logout(request)
    return redirect("signin")


def login_page(request):
    """View to display signin page containing a signin form to allow a 
    registered user to log and return home page. If the username or the 
    password are not valid, it display a message to allow the user to enter 
    new username or password
    """
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
                message = "Identifiants invalides, veuillez recommencer."
    return render(
        request, "users/signin.html", context={"form": form, "message": message}
    )


def signup_page(request):
    """View used to return signup page containing a signup form  and allows the user to register"""
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')
    return render(request, "users/signup.html", context={"form": form})
