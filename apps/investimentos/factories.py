import factory
from factory.django import DjangoModelFactory
from apps.investimentos.models import TipoInvestimento, Investimento
from apps.clientes.factories import ClienteFactory
from datetime import date
from decimal import Decimal


class TipoInvestimentoFactory(DjangoModelFactory):
    class Meta:
        model = TipoInvestimento
        django_get_or_create = ("nome",)

    nome = factory.Sequence(lambda n: f"Ativo Tipo {n}")
    descricao = "Aplicação financeira de renda fixa/variável"


class InvestimentoFactory(DjangoModelFactory):
    class Meta:
        model = Investimento

    cliente = factory.SubFactory(ClienteFactory)
    tipo = factory.SubFactory(TipoInvestimentoFactory)
    valor_investido = Decimal("50000.00")
    data_aplicacao = factory.LazyFunction(date.today)
