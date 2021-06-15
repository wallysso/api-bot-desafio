"""apibot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from apibot import viewsets as apibotviewsets


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mensagem/', apibotviewsets.MensagemViewSet.as_view({'get': 'list'})),
    path('api/mensagem/<int:pk>', apibotviewsets.MensagemAtualizar),
    path('api/mensagem/nao-enviadas', apibotviewsets.MensagemNaoEnviadas.as_view()),
    path('api/mensagem/lida/<int:pk>', apibotviewsets.MensagemLida),
    path('api/usuario/', apibotviewsets.UsuarioViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/usuario/<int:pk>', apibotviewsets.UsuarioCadastrar),
    path('api/usuariover/<int:pk>', apibotviewsets.UsuarioExiste),
]

