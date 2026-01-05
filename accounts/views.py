from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student
from django.contrib import auth


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")  # Fixed: matches HTML name attribute
        last_name = request.POST.get("lastname")    # Fixed: matches HTML name attribute
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Check if username already exists
        if Student.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, "accounts/register.html")
        
        # Check if email already exists
        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return render(request, "accounts/register.html")
        
        try:
            # Create new user
            new_user = Student.objects.create_user(
                username=username,   
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password  # create_user automatically hashes the password
            )
            new_user.set_password(password)  # Hash the password 
            messages.success(request, "Account created successfully! Welcome to DareSwap!")
            return redirect("home")  # This will redirect to home page
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, "accounts/register.html")
    
    return render(request, "accounts/register.html")

#==========================login==========================
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful! Welcome back to DareSwap!")
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, "accounts/login.html")

#==========================logout==========================
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.") 
    return redirect("home")  # Redirect to home page after logout
