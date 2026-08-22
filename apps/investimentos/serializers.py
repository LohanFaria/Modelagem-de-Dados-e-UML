from rest_framework import serializers
from .models import TipoInvestimento, Investimento


class TipoInvestimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInvestimento
        fields = ["id", "nome", "descricao"]


class InvestimentoSerializer(serializers.ModelSerializer):
    tipo_nome = serializers.ReadOnlyField(source="tipo.nome")
    cliente_nome = serializers.ReadOnlyField(source="cliente.nome")

    class Meta:
        model = Investimento
        fields = ["id", "cliente", "cliente_nome", "tipo", "tipo_nome", "valor_investido", "data_aplicacao", "criado_em"]
