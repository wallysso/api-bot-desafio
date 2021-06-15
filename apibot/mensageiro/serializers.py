from rest_framework import serializers

from apibot.mensageiro import models


class MensagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mensagem
        fields = '__all__'


class UsuarioCadastradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UsuarioCadastrado
        fields = '__all__'
