from rest_framework import viewsets, permissions
from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """API REST para consulta e cadastro de clientes com inlines."""
    queryset = Cliente.objects.prefetch_related("telefones", "emails", "contas__saldos", "investimentos").all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["nome", "cpf"]
    ordering_fields = ["nome", "criado_em"]
