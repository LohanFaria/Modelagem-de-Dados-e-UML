from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from apps.clientes.models import Cliente
from . import queries


def eh_gestor_ou_auditor(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=["Gestor", "Auditor"]).exists()


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def painel_relatorios(request):
    qualidade = queries.painel_qualidade_dados()
    investimentos = queries.total_investido_por_tipo()
    return render(request, "relatorios/painel.html", {
        "qualidade": qualidade,
        "investimentos": investimentos,
    })


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def carteira_cliente(request):
    cliente_id = request.GET.get("cliente_id")
    dados_carteira = None
    if cliente_id:
        dados_carteira = queries.carteira_completa_cliente(cliente_id)
    
    clientes_lista = Cliente.objects.only("id", "nome", "cpf").order_by("nome")
    return render(request, "relatorios/carteira.html", {
        "dados_carteira": dados_carteira,
        "clientes_lista": clientes_lista,
        "cliente_selecionado": int(cliente_id) if cliente_id and cliente_id.isdigit() else None,
    })


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def investimentos_por_tipo(request):
    dados = queries.total_investido_por_tipo()
    return render(request, "relatorios/investimentos_tipo.html", {"dados": dados})


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def evolucao_saldo(request):
    cliente_id = request.GET.get("cliente_id")
    saldos = queries.evolucao_saldo_contas(cliente_id)
    clientes_lista = Cliente.objects.only("id", "nome", "cpf").order_by("nome")
    return render(request, "relatorios/evolucao_saldo.html", {
        "saldos": saldos,
        "clientes_lista": clientes_lista,
    })


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def produtividade_funcionarios(request):
    dados = queries.produtividade_contatos()
    return render(request, "relatorios/produtividade.html", {"dados": dados})


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def clientes_sem_contato(request):
    dias = int(request.GET.get("dias", 30))
    clientes = queries.clientes_inativos(dias=dias)
    return render(request, "relatorios/reativacao.html", {
        "clientes": clientes,
        "dias": dias,
    })


@login_required
@user_passes_test(eh_gestor_ou_auditor)
def qualidade_dados(request):
    dados = queries.painel_qualidade_dados()
    return render(request, "relatorios/qualidade_dados.html", {"dados": dados})
