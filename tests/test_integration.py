import pytest
from decimal import Decimal
from apps.clientes.factories import ClienteFactory, ContaBancariaFactory, SaldoHistoricoFactory
from apps.investimentos.factories import InvestimentoFactory, TipoInvestimentoFactory
from apps.relacionamento.factories import ContatoFactory


@pytest.mark.django_db
def test_fluxo_completo_integrado_cliente():
    cliente = ClienteFactory(nome="Valeria Nunes")
    conta1 = ContaBancariaFactory(cliente=cliente, banco="XPTO")
    conta2 = ContaBancariaFactory(cliente=cliente, banco="Itaú")

    SaldoHistoricoFactory(conta=conta1, saldo=Decimal("20000.00"))
    SaldoHistoricoFactory(conta=conta2, saldo=Decimal("30000.00"))

    tipo = TipoInvestimentoFactory(nome="Fundo Multimercado Plus")
    InvestimentoFactory(cliente=cliente, tipo=tipo, valor_investido=Decimal("50000.00"))

    contato = ContatoFactory(cliente=cliente)

    assert cliente.contas.count() == 2
    assert cliente.saldo_atual_consolidado() == Decimal("50000.00")
    assert cliente.total_investido() == Decimal("50000.00")
    assert cliente.contatos.count() == 1
