from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bem-vindo ao River Raid!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('game.urls')),
    path('', home),  # Adiciona a rota padrão
]
