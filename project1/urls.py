from django.contrib import admin
from django.urls import path, include
from home import views

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('saraswat/', admin.site.urls),
    path("", include("home.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("accounts/",include("accounts.urls")),
    

]

urlpatterns +=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
