from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from .models import DareExchange
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

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



#======================================creating a dare=========================================================




#===============================================================================read dares=============================================================================================================

@login_required
def current_dares(request):

    # Show ONLY unaccepted dares NOT created by current user
    dares = DareExchange.objects.filter(
        is_accepted=False
    ).exclude(user=request.user).order_by("-id")

    # Statistics
    total_dares = dares.count()
    unique_creators = dares.values('user').distinct().count()

    context = {
        'dares': dares,
        'total_dares': total_dares,
        'unique_creators': unique_creators,
        "page": "feed",

    }

    return render(request, "home/current_dares.html", context)



#===============================================================================delete dare==================================================================================================================

#===============================================================================edit dare===================================================================================================================

#acceptdares
@login_required
def my_accepted_dares(request):
    dares = DareExchange.objects.filter(
        accepted_by=request.user
    )

    return render(request, "home/my_accepted_dares.html", {
        "dares": dares
    })
@login_required
def accept_dare(request, id):
    dare = get_object_or_404(
        DareExchange,
        id=id,
        is_accepted=False
    )

    # prevent accepting own dare
    if dare.user == request.user:
        return redirect("current_dares")

    dare.is_accepted = True
    dare.accepted_by = request.user
    dare.save()

    return redirect("my_accepted_dares")

#complete dares
@login_required
def complete_dare(request, id):
    dare = get_object_or_404(
        DareExchange,
        id=id,
        accepted_by=request.user,
        is_completed=False
    )

    dare.is_completed = True
    dare.save()

    # ✅ SUCCESS MESSAGE
    messages.success(request, "Dare completed successfully 🎉")

    # ✅ REDIRECT BACK TO DASHBOARD
    return redirect("dashboard")

def get_badge(points):
    """
    Assign badges to users based on their completed dare count.
    
    Args:
        points (int): Number of completed dares
    
    Returns:
        str: Badge name or None if no badge earned
    """
    if points >= 50:
        return "Legend"
    elif points >= 30:
        return "Master"
    elif points >= 20:
        return "Champion"
    elif points >= 10:
        return "Expert"
    elif points >= 5:
        return "Rising Star"
    elif points >= 1:
        return "Novice"
    else:
        return None

def leaderboard(request):
    """
    Display leaderboard of users ranked by completed dares.
    """
    # Get users with their completed dare counts
    users = (
        User.objects
        .annotate(
            completed_count=Count(
                "accepted_dares",
                filter=Q(accepted_dares__is_completed=True)
            )
        )
        .filter(completed_count__gt=0)  # Only users with at least 1 completed dare
        .order_by("-completed_count")  # Highest to lowest
    )

    # Build leaderboard data
    leaderboard_data = []
    for user in users:
        leaderboard_data.append({
            "user": user,
            "points": user.completed_count,
            "badge": get_badge(user.completed_count)
        })

    return render(request, "home/leaderboard.html", {
        "leaderboard": leaderboard_data
    })