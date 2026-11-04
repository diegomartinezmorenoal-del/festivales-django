from django.shortcuts import render
from .models import Festival

def index(request):
    # Vista principal
    return render(request, 'gestion/index.html')

def lista_festivales(request):
    # Lista todos los festivales ordenados por fecha de inicio, mostrando
   
    festivales = (
        Festival.objects
        .select_related('recinto')
        .prefetch_related('patrocinadores', 'escenarios')
        .order_by('fecha_inicio')
    )
    return render(request, 'gestion/lista_festivales.html', {'festivales': festivales})