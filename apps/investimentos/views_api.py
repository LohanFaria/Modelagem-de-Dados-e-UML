from rest_framework import viewsets, permissions
from .models import TipoInvestimento, Investimento
from .serializers import TipoInvestimentoSerializer, InvestimentoSerializer


class TipoInvestimentoViewSet(viewsets.ModelViewSet):
    queryset = TipoInvestimento.objects.all()
    serializer_class = TipoInvestimentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvestimentoViewSet(viewsets.ModelViewSet):
    queryset = Investimento.objects.select_related("cliente", "tipo").all()
    serializer_class = InvestimentoSerializer
    permission_classes = [permissions.IsAuthenticated]
