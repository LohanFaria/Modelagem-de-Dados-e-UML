from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Max, Q, F, Value, DecimalField
from django.db.models.functions import Coalesce
from apps.clientes.models import Cliente, ContaBancaria, SaldoHistorico
from apps.investimentos.models import Investimento, TipoInvestimento
from apps.relacionamento.models import Contato, ContatoQuarentena, Funcionario


def total_investido_por_tipo():
    """Agregação do total investido por tipo de investimento com percentual."""
    total_geral = Investimento.objects.aggregate(total=Sum("valor_investido"))["total"] or Decimal("0.00")
    
    qs = (
        TipoInvestimento.objects.annotate(
            total=Coalesce(Sum("investimentos__valor_investido"), Value(Decimal("0.00")), output_field=DecimalField()),
            qtd=Count("investimentos"),
        )
        .order_by("-total")
    )
    
    resultados = []
    for item in qs:
        pct = (item.total / total_geral * 100) if total_geral > 0 else Decimal("0.0")
        resultados.append({
            "tipo": item.nome,
            "total": item.total,
            "qtd": item.qtd,
            "percentual": round(pct, 2),
        })
    return {"total_geral": total_geral, "itens": resultados}


def carteira_completa_cliente(cliente_id: int):
    """Visão consolidada da carteira: contas, saldos, investimentos e contatos."""
    cliente = Cliente.objects.prefetch_related(
        "contas__saldos",
        "investimentos__tipo",
        "contatos__funcionario",
        "contatos__assunto",
        "contatos__forma",
    ).filter(id=cliente_id).first()
    
    if not cliente:
        return None

    contas_info = []
    saldo_total = Decimal("0.00")
    for conta in cliente.contas.all():
        ultimo_saldo = conta.saldos.order_by("-data_saldo").first()
        valor = ultimo_saldo.saldo if ultimo_saldo else Decimal("0.00")
        saldo_total += valor
        contas_info.append({
            "banco": conta.banco,
            "agencia": conta.agencia,
            "conta": conta.conta,
            "saldo_atual": valor,
            "data_saldo": ultimo_saldo.data_saldo if ultimo_saldo else None,
        })

    investimentos_info = []
    investimento_total = Decimal("0.00")
    for inv in cliente.investimentos.all():
        investimento_total += inv.valor_investido
        investimentos_info.append({
            "tipo": inv.tipo.nome,
            "valor": inv.valor_investido,
            "data_aplicacao": inv.data_aplicacao,
        })

    ultimos_contatos = [
        {
            "data": c.data_contato,
            "funcionario": c.funcionario.nome,
            "assunto": c.assunto.nome,
            "forma": c.forma.nome,
            "observacao": c.observacao,
        }
        for c in cliente.contatos.order_by("-data_contato")[:10]
    ]

    return {
        "cliente": cliente,
        "contas": contas_info,
        "saldo_total": saldo_total,
        "investimentos": investimentos_info,
        "investimento_total": investimento_total,
        "patrimonio_total": saldo_total + investimento_total,
        "ultimos_contatos": ultimos_contatos,
    }


def evolucao_saldo_contas(cliente_id: int = None):
    """Série histórica de saldos de contas bancárias."""
    qs = SaldoHistorico.objects.select_related("conta__cliente").order_by("-data_saldo")
    if cliente_id:
        qs = qs.filter(conta__cliente_id=cliente_id)
    return qs[:100]


def produtividade_contatos(data_inicio=None, data_fim=None):
    """Produtividade de atendimento por funcionário e por assunto."""
    qs = Contato.objects.all()
    if data_inicio:
        qs = qs.filter(data_contato__gte=data_inicio)
    if data_fim:
        qs = qs.filter(data_contato__lte=data_fim)

    por_funcionario = (
        qs.values("funcionario__nome")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    por_assunto = (
        qs.values("assunto__nome")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return {
        "por_funcionario": por_funcionario,
        "por_assunto": por_assunto,
        "total_atendimentos": qs.count(),
    }


def clientes_inativos(dias: int = 30):
    """Clientes sem nenhum contato registrado há mais de N dias."""
    limite = date.today() - timedelta(days=dias)
    
    # Clientes com último contato anterior à data limite ou sem nenhum contato
    qs = Cliente.objects.annotate(
        ultimo_contato=Max("contatos__data_contato")
    ).filter(
        Q(ultimo_contato__lt=limite) | Q(ultimo_contato__isnull=True)
    ).order_by("ultimo_contato")
    
    return qs


def painel_qualidade_dados():
    """Diagnóstico de qualidade cadastral e quarentena."""
    total_clientes = Cliente.objects.count()
    sem_telefone = Cliente.objects.filter(telefones__isnull=True).count()
    sem_email = Cliente.objects.filter(emails__isnull=True).count()
    sem_investimento = Cliente.objects.filter(investimentos__isnull=True).count()
    sem_conta = Cliente.objects.filter(contas__isnull=True).count()
    
    quarentena_pendente = ContatoQuarentena.objects.filter(resolvido=False).count()
    quarentena_resolvida = ContatoQuarentena.objects.filter(resolvido=True).count()

    return {
        "total_clientes": total_clientes,
        "sem_telefone": sem_telefone,
        "sem_email": sem_email,
        "sem_investimento": sem_investimento,
        "sem_conta": sem_conta,
        "quarentena_pendente": quarentena_pendente,
        "quarentena_resolvida": quarentena_resolvida,
    }
