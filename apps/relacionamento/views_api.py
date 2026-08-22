from rest_framework import viewsets, permissions
from .models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena
from .serializers import (
    FuncionarioSerializer,
    FormaContatoSerializer,
    AssuntoSerializer,
    ContatoSerializer,
    ContatoQuarentenaSerializer,
)


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.select_related("cliente", "funcionario", "forma", "assunto").all()
    serializer_class = ContatoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContatoQuarentenaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContatoQuarentena.objects.all()
    serializer_class = ContatoQuarentenaSerializer
    permission_classes = [permissions.IsAuthenticated]
