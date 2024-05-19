from django.urls import path
from . import views

urlpatterns = [
    path('', views.movielog),
    path('register/' , views.movieregister),
    path('home/', views.moviehome),
    path('personal/', views.moviepersonal)
]
