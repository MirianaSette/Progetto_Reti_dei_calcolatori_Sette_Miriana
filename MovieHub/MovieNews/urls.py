from django.urls import path
from . import views

urlpatterns = [
    path('', views.moviehome, name = "home"),
    path('login/', views.movielog, name = 'login'),
    path('register/', views.movieregister, name = 'reg'),
    path('personal/', views.moviepersonal, name = "personal")
]
