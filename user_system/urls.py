from django.urls import path
from user_system import views


app_name = "user_system"

urlpatterns = [
    path('', views.home_screen, name="home_screen"),
    path('login', views.login, name="login"),
    path('information', views.information, name="information"),
]
