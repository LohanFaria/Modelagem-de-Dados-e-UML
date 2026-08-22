import pytest
from decimal import Decimal
from django.db import IntegrityError, transaction
from datetime import date
from apps.clientes.models import Cliente
from apps.investimentos.models import TipoInvestimento, Investimento


@pytest.mark.django_db
def test_criacao_investimento_e_relacionamento():
    cliente = Cliente.objects.create(nome="Igor Santos", cpf="529.982.247-25")
    tipo = TipoInvestimento.objects.create(nome="Tesouro IPCA+ 2035", descricao="Título público atrelado à inflação")
    inv = Investimento.objects.create(
        cliente=cliente,
        tipo=tipo,
        valor_investido=Decimal("25000.00"),
        data_aplicacao=date(2026, 1, 15),
    )

    assert inv.cliente == cliente
    assert inv.tipo == tipo
    assert str(tipo) == "Tesouro IPCA+ 2035"
    assert "Igor Santos" in str(inv)
    assert "25" in str(inv)
    assert cliente.total_investido() == Decimal("25000.00")



@pytest.mark.django_db
def test_tipo_investimento_unicidade_nome():
    TipoInvestimento.objects.create(nome="Ações B3")
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            TipoInvestimento.objects.create(nome="Ações B3")


@pytest.mark.django_db
def test_exclusao_tipo_investimento_bloqueada_protect():
    cliente = Cliente.objects.create(nome="Julia Martins", cpf="529.982.247-25")
    tipo = TipoInvestimento.objects.create(nome="LCI Imobiliária")
    Investimento.objects.create(cliente=cliente, tipo=tipo, valor_investido=Decimal("15000.00"))

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            tipo.delete()
