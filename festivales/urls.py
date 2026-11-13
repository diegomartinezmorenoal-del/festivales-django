from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion.urls')),
]
handler400 = 'gestion.views.error_400'
handler403 = 'gestion.views.error_403'
handler404 = 'gestion.views.error_404'
handler500 = 'gestion.views.error_500'