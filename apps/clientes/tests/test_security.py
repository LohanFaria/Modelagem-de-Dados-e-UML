import pytest
from django.contrib.auth.models import User, Group
from django.test import RequestFactory
from django.contrib.admin.sites import site
from apps.clientes.models import Cliente
from apps.clientes.admin import ClienteAdmin


@pytest.mark.django_db
def test_consultor_nao_tem_permissao_delete_cliente():
    user = User.objects.create_user(username="consultor_sec", password="p1")
    grupo_consultor, _ = Group.objects.get_or_create(name="Consultor")
    user.groups.add(grupo_consultor)

    cliente = Cliente.objects.create(nome="Gabriel Pires", cpf="529.982.247-25")
    admin = ClienteAdmin(Cliente, site)
    
    request = RequestFactory().post(f"/admin/clientes/cliente/{cliente.id}/delete/")
    request.user = user

    assert admin.has_delete_permission(request, cliente) is False


@pytest.mark.django_db
def test_gestor_tem_permissao_delete_cliente():
    from django.contrib.auth.models import Permission
    user = User.objects.create_user(username="gestor_sec", password="p1", is_staff=True)
    grupo_gestor, _ = Group.objects.get_or_create(name="Gestor")
    perm = Permission.objects.get(codename="delete_cliente")
    grupo_gestor.permissions.add(perm)
    user.groups.add(grupo_gestor)

    cliente = Cliente.objects.create(nome="Helena Souza", cpf="529.982.247-25")
    admin = ClienteAdmin(Cliente, site)
    
    request = RequestFactory().post(f"/admin/clientes/cliente/{cliente.id}/delete/")
    request.user = user

    assert admin.has_delete_permission(request, cliente) is True

