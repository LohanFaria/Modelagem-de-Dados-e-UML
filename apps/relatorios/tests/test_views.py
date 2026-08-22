import pytest
from django.contrib.auth.models import User, Group
from django.test import Client
from django.urls import reverse
from apps.clientes.factories import ClienteFactory


@pytest.mark.django_db
def test_consultor_recebe_redirect_ou_bloqueio_relatorios():
    client = Client()
    user = User.objects.create_user(username="consultor_rel", password="p1")
    grupo, _ = Group.objects.get_or_create(name="Consultor")
    user.groups.add(grupo)
    client.force_login(user)

    url = reverse("relatorios:painel")
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_gestor_acessa_todos_os_relatorios():
    client = Client()
    user = User.objects.create_user(username="gestor_rel", password="p1")
    grupo, _ = Group.objects.get_or_create(name="Gestor")
    user.groups.add(grupo)
    client.force_login(user)

    cli = ClienteFactory()

    rotas = [
        ("relatorios:painel", {}),
        ("relatorios:investimentos_tipo", {}),
        ("relatorios:reativacao", {}),
        ("relatorios:produtividade", {}),
        ("relatorios:evolucao_saldo", {}),
        ("relatorios:qualidade_dados", {}),
    ]

    for rota, params in rotas:
        url = reverse(rota)
        response = client.get(url, params)
        assert response.status_code == 200, f"Falha ao acessar rota {rota}"

    # Carteira do cliente via query parameter
    url_carteira = reverse("relatorios:carteira_cliente")
    resp_carteira = client.get(url_carteira, {"cliente_id": cli.id})
    assert resp_carteira.status_code == 200


@pytest.mark.django_db
def test_exportacao_relatorios_para_excel():
    client = Client()
    user = User.objects.create_user(username="gestor_export", password="p1")
    grupo, _ = Group.objects.get_or_create(name="Gestor")
    user.groups.add(grupo)
    client.force_login(user)

    rotas_exportacao = [
        "relatorios:exportar_investimentos",
        "relatorios:exportar_reativacao",
        "relatorios:exportar_produtividade",
    ]

    for rota in rotas_exportacao:
        url = reverse(rota)
        resp = client.get(url)
        assert resp.status_code == 200
        assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in resp["Content-Type"]
        assert len(resp.content) > 0


@pytest.mark.django_db
def test_usuario_anonimo_redirecionado_para_login():
    client = Client()
    url = reverse("relatorios:painel")
    response = client.get(url)
    assert response.status_code == 302
    assert "/admin/login/" in response.url
