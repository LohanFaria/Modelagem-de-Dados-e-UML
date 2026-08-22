import pytest
from datetime import date
from django.db import IntegrityError, transaction
from apps.clientes.models import Cliente
from apps.relacionamento.models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena


@pytest.mark.django_db
def test_criacao_contato_e_quarentena():
    cliente = Cliente.objects.create(nome="Julia Farias", cpf="529.982.247-25")
    func = Funcionario.objects.create(nome="Lucas Atendente", matricula="FUNC-001")
    forma = FormaContato.objects.create(nome="WhatsApp")
    assunto = Assunto.objects.create(nome="Revisão Trimestral")

    contato = Contato.objects.create(
        cliente=cliente,
        funcionario=func,
        forma=forma,
        assunto=assunto,
        data_contato=date(2026, 8, 10),
        observacao="Cliente solicitou aumento de aporte."
    )
    assert contato.cliente == cliente
    assert cliente.contatos.count() == 1
    assert str(func) == "Lucas Atendente"
    assert str(forma) == "WhatsApp"
    assert str(assunto) == "Revisão Trimestral"
    assert "10/08/2026" in str(contato)


    # Quarentena
    quarentena = ContatoQuarentena.objects.create(
        linha_origem={"cpf": "999.999.999-99", "nome": "Desconhecido"},
        motivo="CLIENTE_INEXISTENTE",
        detalhe="CPF inexistente na base."
    )
    assert quarentena.resolvido is False
    assert "CPF não encontrado" in str(quarentena)


    quarentena.resolvido = True
    quarentena.save()
    assert ContatoQuarentena.objects.filter(resolvido=True).count() == 1


@pytest.mark.django_db
def test_funcionario_unicidade_matricula():
    Funcionario.objects.create(nome="Atendente A", matricula="F-01")
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Funcionario.objects.create(nome="Atendente B", matricula="F-01")


@pytest.mark.django_db
def test_exclusao_funcionario_bloqueada_protect():
    cliente = Cliente.objects.create(nome="Katia Pires", cpf="529.982.247-25")
    func = Funcionario.objects.create(nome="Marcos Consultor", matricula="F-02")
    forma = FormaContato.objects.create(nome="Telefone")
    assunto = Assunto.objects.create(nome="Dúvidas de Carteira")

    Contato.objects.create(cliente=cliente, funcionario=func, forma=forma, assunto=assunto, data_contato=date(2026, 8, 1))

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            func.delete()

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            forma.delete()

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            assunto.delete()
