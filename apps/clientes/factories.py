import factory
from factory.django import DjangoModelFactory
from apps.clientes.models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from datetime import date
from decimal import Decimal


class ClienteFactory(DjangoModelFactory):
    class Meta:
        model = Cliente
        django_get_or_create = ("cpf",)

    nome = factory.Faker("name", locale="pt_BR")
    cpf = factory.Sequence(lambda n: f"{n:03d}.{n:03d}.{n:03d}-{n%100:02d}")


class TelefoneFactory(DjangoModelFactory):
    class Meta:
        model = Telefone

    cliente = factory.SubFactory(ClienteFactory)
    numero = factory.Sequence(lambda n: f"(11) 9{n:04d}-{n:04d}")
    tipo = "CELULAR"


class EmailFactory(DjangoModelFactory):
    class Meta:
        model = Email

    cliente = factory.SubFactory(ClienteFactory)
    endereco = factory.LazyAttribute(lambda o: f"{o.cliente.nome.lower().replace(' ', '.')}@example.com")
    principal = True


class ContaBancariaFactory(DjangoModelFactory):
    class Meta:
        model = ContaBancaria

    cliente = factory.SubFactory(ClienteFactory)
    banco = "Banco XPTO"
    agencia = factory.Sequence(lambda n: f"{n:04d}")
    conta = factory.Sequence(lambda n: f"{n:05d}-1")


class SaldoHistoricoFactory(DjangoModelFactory):
    class Meta:
        model = SaldoHistorico

    conta = factory.SubFactory(ContaBancariaFactory)
    data_saldo = factory.LazyFunction(date.today)
    saldo = factory.LazyAttribute(lambda o: Decimal("15000.00"))
