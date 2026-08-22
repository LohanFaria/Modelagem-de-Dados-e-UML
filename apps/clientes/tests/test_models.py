import pytest
from django.db import IntegrityError, transaction
from datetime import date
from decimal import Decimal
from apps.clientes.models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from apps.investimentos.models import Investimento, TipoInvestimento
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_cliente_unicidade_cpf():
    Cliente.objects.create(nome="Ana Silva", cpf="529.982.247-25")
    with pytest.raises((IntegrityError, ValidationError)):
        with transaction.atomic():
            Cliente.objects.create(nome="Ana Outra", cpf="529.982.247-25")


@pytest.mark.django_db
def test_cliente_str_e_formatacao():
    cliente = Cliente.objects.create(nome="Eduardo Lima", cpf="111.444.777-35")
    assert str(cliente) == "Eduardo Lima (111.444.777-35)"


@pytest.mark.django_db
def test_conta_bancaria_unicidade_composta():
    cliente = Cliente.objects.create(nome="Fernanda Dias", cpf="529.982.247-25")
    ContaBancaria.objects.create(cliente=cliente, banco="Banco Itaú", agencia="1000", conta="55555-5")

    # Mesma conta/agência/banco deve falhar
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            ContaBancaria.objects.create(cliente=cliente, banco="Banco Itaú", agencia="1000", conta="55555-5")

    # Mesmo número de conta mas banco diferente é permitido
    conta2 = ContaBancaria.objects.create(cliente=cliente, banco="Bradesco", agencia="1000", conta="55555-5")
    assert conta2.id is not None


@pytest.mark.django_db
def test_saldo_historico_unicidade_conta_data():
    cliente = Cliente.objects.create(nome="Bruno Costa", cpf="529.982.247-25")
    conta = ContaBancaria.objects.create(cliente=cliente, banco="XPTO", agencia="0001", conta="12345-6")
    
    SaldoHistorico.objects.create(conta=conta, data_saldo=date(2026, 8, 1), saldo=Decimal("1000.00"))
    
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            SaldoHistorico.objects.create(conta=conta, data_saldo=date(2026, 8, 1), saldo=Decimal("2000.00"))

    # Mesma conta com data diferente é permitido
    saldo_novo = SaldoHistorico.objects.create(conta=conta, data_saldo=date(2026, 8, 2), saldo=Decimal("2000.00"))
    assert saldo_novo.id is not None


@pytest.mark.django_db
def test_exclusao_cliente_remove_dependentes_em_cascata():
    cliente = Cliente.objects.create(nome="Carlos Dias", cpf="529.982.247-25")
    tel = Telefone.objects.create(cliente=cliente, numero="(11) 98765-4321")
    email = Email.objects.create(cliente=cliente, endereco="carlos@example.com", principal=True)
    conta = ContaBancaria.objects.create(cliente=cliente, banco="XPTO", agencia="0001", conta="99999-1")
    saldo = SaldoHistorico.objects.create(conta=conta, data_saldo=date(2026, 8, 1), saldo=Decimal("500.00"))

    assert str(tel) == "(11) 98765-4321 (Celular)"
    assert str(email) == "carlos@example.com"
    assert str(conta) == "XPTO Ag 0001 Cc 99999-1"
    assert "500.00" in str(saldo)
    assert "01/08/2026" in str(saldo)



    cliente_id = cliente.id
    conta_id = conta.id
    cliente.delete()

    assert not Cliente.objects.filter(id=cliente_id).exists()
    assert not Telefone.objects.filter(cliente_id=cliente_id).exists()
    assert not Email.objects.filter(cliente_id=cliente_id).exists()
    assert not ContaBancaria.objects.filter(id=conta_id).exists()
    assert not SaldoHistorico.objects.filter(conta_id=conta_id).exists()


@pytest.mark.django_db
def test_exclusao_cliente_com_investimento_bloqueada_protect():
    cliente = Cliente.objects.create(nome="Daniela Rocha", cpf="529.982.247-25")
    tipo = TipoInvestimento.objects.create(nome="CDB 120% CDI")
    Investimento.objects.create(cliente=cliente, tipo=tipo, valor_investido=Decimal("50000.00"))

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            cliente.delete()
