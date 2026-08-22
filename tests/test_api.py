import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.clientes.factories import ClienteFactory, ContaBancariaFactory
from apps.investimentos.factories import TipoInvestimentoFactory, InvestimentoFactory
from apps.relacionamento.factories import FuncionarioFactory, FormaContatoFactory, AssuntoFactory, ContatoFactory
from apps.relacionamento.models import ContatoQuarentena


@pytest.mark.django_db
def test_api_clientes_anonimo_bloqueado():
    client = APIClient()
    resp = client.get("/api/v1/clientes/")
    assert resp.status_code in [401, 403]


@pytest.mark.django_db
def test_api_clientes_autenticado_retorna_lista():
    client = APIClient()
    user = User.objects.create_user(username="api_user", password="p1")
    client.force_authenticate(user=user)

    cli = ClienteFactory(nome="Marina Silva", cpf="529.982.247-25")
    ContaBancariaFactory(cliente=cli, banco="XPTO", agencia="0001", conta="99112-3")

    resp = client.get("/api/v1/clientes/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert data[0]["nome"] == "Marina Silva"
    assert len(data[0]["contas"]) == 1


@pytest.mark.django_db
def test_api_criar_cliente():
    client = APIClient()
    user = User.objects.create_user(username="api_creator", password="p1")
    client.force_authenticate(user=user)

    payload = {
        "nome": "Roberto Carlos",
        "cpf": "111.444.777-35",
    }
    resp = client.post("/api/v1/clientes/", payload, format="json")
    assert resp.status_code == 201
    assert resp.json()["nome"] == "Roberto Carlos"


@pytest.mark.django_db
def test_api_investimentos_e_tipos():
    client = APIClient()
    user = User.objects.create_user(username="api_inv", password="p1")
    client.force_authenticate(user=user)

    cli = ClienteFactory()
    tipo = TipoInvestimentoFactory(nome="CDB Prefixado 120%")
    InvestimentoFactory(cliente=cli, tipo=tipo, valor_investido=Decimal("50000.00"))

    resp_tipos = client.get("/api/v1/tipos-investimento/")
    assert resp_tipos.status_code == 200
    assert len(resp_tipos.json()) >= 1

    resp_inv = client.get("/api/v1/investimentos/")
    assert resp_inv.status_code == 200
    assert len(resp_inv.json()) >= 1


@pytest.mark.django_db
def test_api_contatos_e_quarentena():
    client = APIClient()
    user = User.objects.create_user(username="api_contatos", password="p1")
    client.force_authenticate(user=user)

    cli = ClienteFactory()
    func = FuncionarioFactory(nome="Atendente Alpha")
    forma = FormaContatoFactory(nome="Telefone")
    assunto = AssuntoFactory(nome="Revisão")
    ContatoFactory(cliente=cli, funcionario=func, forma=forma, assunto=assunto)

    ContatoQuarentena.objects.create(
        linha_origem={"cpf": "000"},
        motivo="CPF_INVALIDO",
        detalhe="Invalido"
    )

    resp_ct = client.get("/api/v1/contatos/")
    assert resp_ct.status_code == 200
    assert len(resp_ct.json()) >= 1

    resp_quar = client.get("/api/v1/quarentena/")
    assert resp_quar.status_code == 200
    assert len(resp_quar.json()) >= 1
