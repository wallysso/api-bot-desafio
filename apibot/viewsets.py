from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apibot.mensageiro import serializers
from apibot.mensageiro import models

class MensagemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MensagensSerializer
    queryset = models.Mensagem.objects.all()


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UsuarioCadastradoSerializer
    queryset = models.UsuarioCadastrado.objects.all()


class MensagemNaoEnviadas(generics.ListAPIView):
    serializer_class = serializers.MensagensSerializer

    def get_queryset(self):
        return models.Mensagem.objects.filter(status=0)

@api_view(['GET', 'PUT'])
def MensagemAtualizar(request, pk):
    try:
        mensagem = models.Mensagem.objects.get(pk=pk)
    except models.Mensagem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.MensagensSerializer(mensagem)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.MensagensSerializer(mensagem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def UsuarioCadastrar(request, pk):
    if request.method == 'GET':
        try:
            usuario = models.UsuarioCadastrado.objects.get(pk=pk)
        except models.UsuarioCadastrado.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UsuarioCadastradoSerializer(usuario)
        return Response(serializer.data)

    if request.method == 'DELETE':
        models.UsuarioCadastrado.objects.filter(fromId=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def MensagemLida(request, pk):
    if request.method == 'GET':
        try:
            mensagem = models.Mensagem.objects.get(pk=pk)
            mensagem.status = 1
            mensagem.save()

            serializer = serializers.MensagensSerializer(mensagem)

            return Response(serializer.data)
        except models.Mensagem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def UsuarioExiste(request, pk):
    if request.method == 'GET':
        usuarios = models.UsuarioCadastrado.objects.filter(fromId=pk)
        
        if len(usuarios) > 0 :
            serializer = serializers.UsuarioCadastradoSerializer(usuarios[0])
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)