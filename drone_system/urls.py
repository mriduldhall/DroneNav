from django.urls import path
from drone_system import views


app_name = "drone_system"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('book', views.book, name="book"),
    path('information', views.information, name="information"),
    path('help', views.help, name="help"),
    path('logout', views.logout, name="logout"),
]
