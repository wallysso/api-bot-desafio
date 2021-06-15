from django.contrib import admin

# Register your models here.
from apibot.mensageiro.models import UsuarioCadastrado, Mensagem


@admin.register(UsuarioCadastrado)
class UsuarioCadastradoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fromId', 'dataCadastro')


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'fromId', 'dataCadastro')
