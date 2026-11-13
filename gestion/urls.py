from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('festivales/', views.lista_festivales, name='lista_festivales'),
    path('festival/<int:id>/', views.detalle_festival, name='detalle_festival'),
    path('artistas/top/', views.top_artistas, name='top_artistas'),
    path('artistas/<str:genero>/', views.artistas_por_genero, name='artistas_por_genero'),
    path('festival/<int:id>/entradas/<str:tipo>/', views.entradas_festival, name='entradas_festival'),
    re_path(r'^festivales/anio/(?P<anio>[0-9]{4})/$', views.festivales_por_anio, name='festivales_por_anio'),
]