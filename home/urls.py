from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name = "home"),
    
    
    path("current_dares/", views.current_dares, name = "current_dares"),
    path("accept_dare/<int:id>/", views.accept_dare, name="accept_dare"),
    path("my_accepted_dares/", views.my_accepted_dares, name="my_accepted_dares"),
    path("complete_dare/<int:id>/", views.complete_dare, name="complete_dare"),
    path("leaderboard", views.leaderboard,name="leaderboard"),
   
   
 ]
