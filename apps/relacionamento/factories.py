import factory
from factory.django import DjangoModelFactory
from apps.relacionamento.models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena
from apps.clientes.factories import ClienteFactory
from datetime import date


class FuncionarioFactory(DjangoModelFactory):
    class Meta:
        model = Funcionario
        django_get_or_create = ("nome",)

    nome = factory.Faker("name", locale="pt_BR")
    matricula = factory.Sequence(lambda n: f"FUNC-{n:04d}")
    ativo = True


class FormaContatoFactory(DjangoModelFactory):
    class Meta:
        model = FormaContato
        django_get_or_create = ("nome",)

    nome = factory.Sequence(lambda n: f"Canal {n}")


class AssuntoFactory(DjangoModelFactory):
    class Meta:
        model = Assunto
        django_get_or_create = ("nome",)

    nome = factory.Sequence(lambda n: f"Assunto {n}")


class ContatoFactory(DjangoModelFactory):
    class Meta:
        model = Contato

    cliente = factory.SubFactory(ClienteFactory)
    funcionario = factory.SubFactory(FuncionarioFactory)
    forma = factory.SubFactory(FormaContatoFactory)
    assunto = factory.SubFactory(AssuntoFactory)
    data_contato = factory.LazyFunction(date.today)
    observacao = "Atendimento de rotina e alinhamento de carteira."
