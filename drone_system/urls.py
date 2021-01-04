from django.urls import path
from drone_system import views


app_name = "drone_system"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('book', views.book, name="book"),
    path('locations', views.locations, name="locations"),
    path('information', views.information, name="information"),
    path('help', views.help, name="help"),
    path('logout', views.logout, name="logout"),
    path('settings', views.settings, name="settings"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('deleteaccount', views.deleteaccount, name="deleteaccount"),
    path('futurebook', views.futurebook, name="futurebook"),
]
