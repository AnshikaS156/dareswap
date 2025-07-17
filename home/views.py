from django.shortcuts import render, redirect
from django.db.models import Count
from .models import DareExchange
from django.contrib.auth.models import User

def home(request):
    # Get statistics for the home page
    total_dares = DareExchange.objects.count()
    unique_creators = DareExchange.objects.values('Name').distinct().count()
    
    # Get recent dares for display (limit to 6 for the home page)
    recent_dares = DareExchange.objects.all().order_by('-id')[:6]
    
    context = {
        'total_dares': total_dares,
        'unique_creators': unique_creators,
        'recent_dares': recent_dares,
    }
    
    return render(request, "home/home.html", context)

def dashboard(request):
    return render(request, "dashboard.html")

#======================================creating a dare=========================================================
def create_dare(request):
    if request.method == "POST":
        
            Name = request.POST.get("Name")
            Email = request.POST.get("Email")
            DareTitle = request.POST.get("DareTitle")
            Description = request.POST.get("Description")
            Difficulty = request.POST.get("Difficulty")
            Category = request.POST.get("Category")
            Deadline = request.POST.get("Deadline")
            Tags = request.POST.get("Tags")

            #creating an object

            
            new_dare = DareExchange(
                Name=Name,
                Email=Email,
                DareTitle=DareTitle,
                Description=Description,
                Difficulty=Difficulty,
                Category=Category,
                Deadline=Deadline,
                Tags=Tags,
            )
            new_dare.save()
            print("new dare added successfully!")

            return redirect("current_dares")
            
        
            
    
    return render(request, "home/create_dare.html")


#===============================================================================read dares=============================================================================================================

def current_dares(request):
    
    dares = DareExchange.objects.all().order_by("-id")
    
    # Calculate statistics
    total_dares = dares.count()
    unique_creators = DareExchange.objects.values('Name').distinct().count()
    
    for dare in dares:
        print(f"Dare: {dare.DareTitle} - {dare.Description}")
    
    context = {
        'dares': dares,
        'total_dares': total_dares,
        'unique_creators': unique_creators,
    }
    
    return render(request, "home/current_dares.html", context)

#===============================================================================delete dare==================================================================================================================
def delete_dare(request,id):
    dare = DareExchange.objects.get(id=id)
    dare.delete()
    return redirect("current_dares")
#===============================================================================edit dare===================================================================================================================
def edit_dare(request, id):
    dare = DareExchange.objects.get(id=id)
    if request.method == "POST":
        dare.Name = request.POST.get("Name")
        dare.Email = request.POST.get("Email")
        dare.DareTitle = request.POST.get("DareTitle")
        dare.Description = request.POST.get("Description")
        dare.Difficulty = request.POST.get("Difficulty")
        dare.Category = request.POST.get("Category")
        dare.Deadline = request.POST.get("Deadline")
        dare.Tags = request.POST.get("Tags")

        
        dare.is_edited = True
        dare.save()
        return redirect("current_dares")

    parameters = {
        "dare": dare
    }
    return render(request, "home/edit_dare.html", parameters)