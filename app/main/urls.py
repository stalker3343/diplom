from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="main"),
    path('login', views.login_request, name="login"),
    path('home', views.home_page, name="home"),
    path('scan', views.scan, name="scan")
]
