from django.shortcuts import render,redirect
from django.contrib.auth.models import User

# Create your views here.
def register(request):

    if request.method=="POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name ")
        email = request.POST.get("email")
        password= request.POST.get("password")

        new_user= User.objects,create(
            username= username,
            first_name=first_name,
            last_name=last_name,
            email=email

        )
        new_user.set_password(password)
        new_user.save()
        return redirect("home")
    return render(request,"accounts/register.html")
