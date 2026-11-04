from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('festivales/', views.lista_festivales, name='lista_festivales'),
    path('festival/<int:id>/', views.detalle_festival, name='detalle_festival'),
    path('artistas/<str:genero>/', views.artistas_por_genero, name='artistas_por_genero'),
    path('festival/<int:id>/entradas/<str:tipo>/', views.entradas_festival, name='entradas_festival'),
]