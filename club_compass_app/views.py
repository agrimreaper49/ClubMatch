from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request, "index.html")

def logout_view(request):
    # Calls a built in method to log the user out and returns to the home screen
    if request.method == "POST":
        logout(request)
        return redirect("/")
    