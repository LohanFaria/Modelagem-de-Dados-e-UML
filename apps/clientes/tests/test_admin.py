import pytest
from decimal import Decimal
from django.contrib.admin.sites import site
from django.test import RequestFactory
from django.contrib.auth.models import User, Group
from apps.clientes.models import Cliente, ContaBancaria, SaldoHistorico
from apps.investimentos.models import Investimento, TipoInvestimento
from apps.clientes.admin import ClienteAdmin


@pytest.mark.django_db
def test_cliente_admin_mascara_cpf_consultor():
    user = User.objects.create_user(username="consultor1", password="p1")
    grupo_consultor, _ = Group.objects.get_or_create(name="Consultor")
    user.groups.add(grupo_consultor)

    cliente = Cliente.objects.create(nome="Eduardo Lima", cpf="529.982.247-25")
    
    admin = ClienteAdmin(Cliente, site)
    request = RequestFactory().get("/admin/clientes/cliente/")
    request.user = user

    admin._current_request = request
    exibicao = admin.exibir_cpf(cliente)
    assert exibicao == "529.***.***-25"


@pytest.mark.django_db
def test_cliente_admin_exibe_cpf_completo_gestor():
    user = User.objects.create_user(username="gestor1", password="p1")
    grupo_gestor, _ = Group.objects.get_or_create(name="Gestor")
    user.groups.add(grupo_gestor)

    cliente = Cliente.objects.create(nome="Fabiana Melo", cpf="529.982.247-25")
    
    admin = ClienteAdmin(Cliente, site)
    request = RequestFactory().get("/admin/clientes/cliente/")
    request.user = user

    admin._current_request = request
    exibicao = admin.exibir_cpf(cliente)
    assert exibicao == "529.982.247-25"


@pytest.mark.django_db
def test_cliente_admin_colunas_calculadas():
    cliente = Cliente.objects.create(nome="Gisele Bundchen", cpf="111.444.777-35")
    conta = ContaBancaria.objects.create(cliente=cliente, banco="XPTO", agencia="0001", conta="11223-4")
    SaldoHistorico.objects.create(conta=conta, data_saldo="2026-08-01", saldo=Decimal("15000.00"))

    tipo = TipoInvestimento.objects.create(nome="CDB 100%")
    Investimento.objects.create(cliente=cliente, tipo=tipo, valor_investido=Decimal("35000.00"))

    admin = ClienteAdmin(Cliente, site)
    saldo_calc = admin.saldo_consolidado_display(cliente)
    inv_calc = admin.total_investido_display(cliente)

    assert "15,000.00" in str(saldo_calc) or "15.000,00" in str(saldo_calc)
    assert "35,000.00" in str(inv_calc) or "35.000,00" in str(inv_calc)
    assert "nome" in admin.search_fields and "cpf" in admin.search_fields
    assert len(admin.inlines) == 3
