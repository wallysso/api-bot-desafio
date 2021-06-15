from django.db import models

# Create your models here.


class UsuarioCadastrado(models.Model):
    fromId = models.BigIntegerField(unique=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.fromId)


class Mensagem(models.Model):
    nome = models.CharField(max_length=200)
    text = models.TextField()
    fromId = models.BigIntegerField()
    dataCadastro = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[
        (0, 'NaoEnviado'),
        (1, 'Enviado'),
    ])

    def __str__(self):
        return self.nome
