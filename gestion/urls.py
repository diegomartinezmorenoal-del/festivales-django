from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('festivales/', views.lista_festivales, name='lista_festivales'),
]