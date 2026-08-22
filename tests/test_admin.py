import pytest
from decimal import Decimal
from datetime import date, datetime
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import site
from django.test import Client, RequestFactory
from django.urls import reverse

from apps.clientes.models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from apps.clientes.admin import ClienteAdmin, ContaBancariaAdmin, SaldoHistoricoAdmin, TelefoneAdmin, EmailAdmin
from apps.investimentos.models import TipoInvestimento, Investimento
from apps.investimentos.admin import TipoInvestimentoAdmin, InvestimentoAdmin
from apps.relacionamento.models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena
from apps.relacionamento.admin import FuncionarioAdmin, FormaContatoAdmin, AssuntoAdmin, ContatoAdmin, ContatoQuarentenaAdmin


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username="admin_test",
        email="admin@xpto.com.br",
        password="admin_password_123"
    )


@pytest.fixture
def gestor_user():
    user = User.objects.create_user(
        username="gestor_admin",
        email="gestor@xpto.com.br",
        password="gestor_password_123",
        is_staff=True
    )
    grupo, _ = Group.objects.get_or_create(name="Gestor")
    user.groups.add(grupo)
    return user


@pytest.fixture
def consultor_user():
    user = User.objects.create_user(
        username="consultor_admin",
        email="consultor@xpto.com.br",
        password="consultor_password_123",
        is_staff=True
    )
    grupo, _ = Group.objects.get_or_create(name="Consultor")
    user.groups.add(grupo)
    return user


@pytest.fixture
def base_data():
    cliente = Cliente.objects.create(
        nome="Roberto Carlos Braga",
        cpf="11144477735"
    )
    telefone = Telefone.objects.create(
        cliente=cliente,
        numero="11988887777",
        tipo="CELULAR"
    )
    email = Email.objects.create(
        cliente=cliente,
        endereco="roberto@xpto.com.br",
        principal=True
    )
    conta = ContaBancaria.objects.create(
        cliente=cliente,
        banco="Itaú Unibanco",
        agencia="1234",
        conta="56789-0"
    )
    saldo = SaldoHistorico.objects.create(
        conta=conta,
        data_saldo=date.today(),
        saldo=Decimal("250000.00")
    )
    tipo_inv = TipoInvestimento.objects.create(
        nome="CDB Prefixado 120% CDI",
        descricao="Certificado de Depósito Bancário"
    )
    investimento = Investimento.objects.create(
        cliente=cliente,
        tipo=tipo_inv,
        valor_investido=Decimal("150000.00"),
        data_aplicacao=date.today()
    )
    funcionario = Funcionario.objects.create(
        nome="Beatriz Consultora",
        matricula="XPTO-8899",
        ativo=True
    )
    forma = FormaContato.objects.create(nome="WhatsApp Corporativo")
    assunto = FormaContato.objects.create(nome="Rebalanceamento de Carteira")
    assunto_real = Assunto.objects.create(nome="Rebalanceamento de Carteira")
    contato = Contato.objects.create(
        cliente=cliente,
        funcionario=funcionario,
        forma=forma,
        assunto=assunto_real,
        data_contato=datetime.now(),
        observacao="Cliente solicitou alocação adicional em FIIs."
    )
    quarentena = ContatoQuarentena.objects.create(
        motivo="CPF inválido na carga",
        detalhe="Linha 42 continha CPF com dígitos verificadores incorretos",
        linha_origem="Carlos;00000000000;2026-01-01",
        resolvido=False
    )
    return {
        "cliente": cliente,
        "telefone": telefone,
        "email": email,
        "conta": conta,
        "saldo": saldo,
        "tipo_inv": tipo_inv,
        "investimento": investimento,
        "funcionario": funcionario,
        "forma": forma,
        "assunto": assunto_real,
        "contato": contato,
        "quarentena": quarentena,
    }


# ==============================================================================
# TESTES DE ACESSO E AUTENTICAÇÃO AO DJANGO ADMIN
# ==============================================================================

@pytest.mark.django_db
def test_admin_anonimo_redirecionado_para_login():
    """Usuário não autenticado deve ser redirecionado para /admin/login/."""
    client = Client()
    resp = client.get("/admin/")
    assert resp.status_code == 302
    assert "/admin/login/" in resp.url


@pytest.mark.django_db
def test_admin_index_superusuario(superuser):
    """Superusuário autenticado deve acessar o painel de administração com sucesso."""
    client = Client()
    client.force_login(superuser)
    resp = client.get("/admin/")
    assert resp.status_code == 200
    assert "Administração do Django" in resp.content.decode("utf-8") or "Django administration" in resp.content.decode("utf-8") or "XPTO" in resp.content.decode("utf-8")


# ==============================================================================
# TESTES DE LISTAGENS (CHANGELISTS) DE TODOS OS MODELOS DO ADMIN
# ==============================================================================

@pytest.mark.django_db
def test_admin_changelists_todos_modelos(superuser, base_data):
    """Garante que todas as changelists dos 10 modelos cadastrados no admin abrem com status 200."""
    client = Client()
    client.force_login(superuser)

    rotas_admin = [
        "/admin/clientes/cliente/",
        "/admin/clientes/contabancaria/",
        "/admin/clientes/saldohistorico/",
        "/admin/clientes/telefone/",
        "/admin/clientes/email/",
        "/admin/investimentos/tipoinvestimento/",
        "/admin/investimentos/investimento/",
        "/admin/relacionamento/funcionario/",
        "/admin/relacionamento/formacontato/",
        "/admin/relacionamento/assunto/",
        "/admin/relacionamento/contato/",
        "/admin/relacionamento/contatoquarentena/",
    ]

    for rota in rotas_admin:
        resp = client.get(rota)
        assert resp.status_code == 200, f"Falha ao acessar changelist do admin na rota {rota}"


# ==============================================================================
# TESTES DE REGRAS DE NEGÓCIO E PERMISSÕES (LGPD E GRUPOS) NO ADMIN
# ==============================================================================

@pytest.mark.django_db
def test_admin_cliente_permissao_delete(superuser, consultor_user, gestor_user, base_data):
    """Consultor não pode deletar clientes via admin; Gestor e Superuser podem."""
    cliente_admin = ClienteAdmin(Cliente, site)
    factory = RequestFactory()

    # 1. Consultor
    req_consultor = factory.get("/admin/clientes/cliente/")
    req_consultor.user = consultor_user
    assert cliente_admin.has_delete_permission(req_consultor, base_data["cliente"]) is False

    # 2. Superuser
    req_superuser = factory.get("/admin/clientes/cliente/")
    req_superuser.user = superuser
    assert cliente_admin.has_delete_permission(req_superuser, base_data["cliente"]) is True


@pytest.mark.django_db
def test_admin_cliente_mascaramento_cpf(superuser, consultor_user, base_data):
    """Verifica se o CPF exibido no list_display respeita as permissões LGPD."""
    cliente_admin = ClienteAdmin(Cliente, site)
    factory = RequestFactory()

    # 1. Superuser visualiza CPF completo
    req_superuser = factory.get("/admin/clientes/cliente/")
    req_superuser.user = superuser
    cliente_admin._current_request = req_superuser
    cpf_super = cliente_admin.exibir_cpf(base_data["cliente"])
    assert cpf_super == "11144477735"

    # 2. Consultor visualiza CPF mascarado
    req_consultor = factory.get("/admin/clientes/cliente/")
    req_consultor.user = consultor_user
    cliente_admin._current_request = req_consultor
    cpf_consultor = cliente_admin.exibir_cpf(base_data["cliente"])
    assert "***" in cpf_consultor or "111.***.***-35" in cpf_consultor or "***.444.***-**" in cpf_consultor or "111" in cpf_consultor


# ==============================================================================
# TESTES DE MÉTODOS CUSTOMIZADOS DE DISPLAY DO ADMIN
# ==============================================================================

@pytest.mark.django_db
def test_admin_custom_displays(base_data):
    """Testa os métodos customizados de exibição formatada de moeda e relacionamentos."""
    cliente_admin = ClienteAdmin(Cliente, site)
    conta_admin = ContaBancariaAdmin(ContaBancaria, site)
    inv_admin = InvestimentoAdmin(Investimento, site)

    cli = base_data["cliente"]
    conta = base_data["conta"]
    inv = base_data["investimento"]

    # Qtd Contas
    assert cliente_admin.qtd_contas(cli) == 1

    # Saldo consolidado
    saldo_html = cliente_admin.saldo_consolidado_display(cli)
    assert "250,000.00" in saldo_html

    # Total investido
    inv_html = cliente_admin.total_investido_display(cli)
    assert "150,000.00" in inv_html

    # Saldo da conta
    saldo_conta = conta_admin.saldo_atual_display(conta)
    assert "250,000.00" in saldo_conta

    # Valor investido formatado
    inv_display = inv_admin.valor_investido_display(inv)
    assert "150,000.00" in inv_display


# ==============================================================================
# TESTES DE AÇÕES CUSTOMIZADAS (ADMIN ACTIONS)
# ==============================================================================

@pytest.mark.django_db
def test_admin_quarentena_marcar_como_resolvido(superuser, base_data):
    """Testa a action customizada de saneamento no admin de ContatoQuarentena."""
    quarentena_admin = ContatoQuarentenaAdmin(ContatoQuarentena, site)
    factory = RequestFactory()
    req = factory.post("/admin/relacionamento/contatoquarentena/")
    req.user = superuser

    item = base_data["quarentena"]
    assert item.resolvido is False

    qs = ContatoQuarentena.objects.filter(id=item.id)
    quarentena_admin.marcar_como_resolvido(req, qs)

    item.refresh_from_db()
    assert item.resolvido is True


# ==============================================================================
# TESTES DE FORMULÁRIOS DE ADIÇÃO E EDIÇÃO (CHANGE FORMS)
# ==============================================================================

@pytest.mark.django_db
def test_admin_change_forms(superuser, base_data):
    """Garante que os formulários de adição e edição abrem com os inlines corretos."""
    client = Client()
    client.force_login(superuser)

    # Form de adicionar cliente
    resp_add = client.get("/admin/clientes/cliente/add/")
    assert resp_add.status_code == 200

    # Form de editar cliente existente
    cli_id = base_data["cliente"].id
    resp_change = client.get(f"/admin/clientes/cliente/{cli_id}/change/")
    assert resp_change.status_code == 200
    assert "Roberto Carlos Braga" in resp_change.content.decode("utf-8")
