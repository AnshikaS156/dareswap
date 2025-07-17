from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name = "home"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("create_dare/", views.create_dare, name = "create_dare"),
    path("current_dares/", views.current_dares, name = "current_dares"),
    path('delete_dare/<int:id>/', views.delete_dare, name="delete_dare"),
    path('edit_dare/<int:id>/',views.edit_dare,name="edit_dare"),

   
]
