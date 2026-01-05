from django.urls import path

from .import views

urlpatterns = [
    
    path('',views.dashboard, name='dashboard'),
    path("create_dare/", views.create_dare, name = "create_dare"),
    path('delete_dare/<int:id>/', views.delete_dare, name="delete_dare"),
    path('edit_dare/<int:id>/',views.edit_dare,name="edit_dare"),
    path('dare/<int:id>/', views.view_dare, name='view_dare'),
    path('ask_ai/', views.ask_ai, name='ask_ai'),

    
]
