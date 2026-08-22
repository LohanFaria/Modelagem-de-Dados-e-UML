import pytest
from decimal import Decimal
from datetime import date, timedelta
from apps.clientes.factories import ClienteFactory, ContaBancariaFactory, SaldoHistoricoFactory
from apps.investimentos.factories import TipoInvestimentoFactory, InvestimentoFactory
from apps.relacionamento.factories import FuncionarioFactory, FormaContatoFactory, AssuntoFactory, ContatoFactory
from apps.relacionamento.models import ContatoQuarentena
from apps.relatorios import queries


@pytest.mark.django_db
def test_queries_total_investido_por_tipo():
    tipo1 = TipoInvestimentoFactory(nome="Renda Fixa CDB")
    tipo2 = TipoInvestimentoFactory(nome="Ações Dividendos")

    cli = ClienteFactory()
    InvestimentoFactory(cliente=cli, tipo=tipo1, valor_investido=Decimal("30000.00"))
    InvestimentoFactory(cliente=cli, tipo=tipo2, valor_investido=Decimal("70000.00"))

    res = queries.total_investido_por_tipo()
    assert res["total_geral"] == Decimal("100000.00")
    assert len(res["itens"]) >= 2
    # Item 1 deve ser o de maior valor (Ações Dividendos = 70%)
    assert res["itens"][0]["tipo"] == "Ações Dividendos"
    assert res["itens"][0]["percentual"] == Decimal("70.00")


@pytest.mark.django_db
def test_queries_carteira_completa_cliente():
    cli = ClienteFactory(nome="Tatiana Ramos")
    conta1 = ContaBancariaFactory(cliente=cli, banco="XPTO")
    SaldoHistoricoFactory(conta=conta1, data_saldo=date(2026, 8, 1), saldo=Decimal("15000.00"))
    # Saldo mais recente que deve ser considerado
    SaldoHistoricoFactory(conta=conta1, data_saldo=date(2026, 8, 5), saldo=Decimal("20000.00"))

    tipo = TipoInvestimentoFactory(nome="LCI Imobiliária")
    InvestimentoFactory(cliente=cli, tipo=tipo, valor_investido=Decimal("50000.00"))

    func = FuncionarioFactory(nome="Ana Atendente")
    forma = FormaContatoFactory(nome="WhatsApp")
    assunto = AssuntoFactory(nome="Revisão")
    ContatoFactory(cliente=cli, funcionario=func, forma=forma, assunto=assunto, data_contato=date(2026, 8, 2))

    carteira = queries.carteira_completa_cliente(cli.id)
    assert carteira is not None
    assert carteira["saldo_total"] == Decimal("20000.00")
    assert carteira["investimento_total"] == Decimal("50000.00")
    assert carteira["patrimonio_total"] == Decimal("70000.00")
    assert len(carteira["ultimos_contatos"]) == 1
    assert carteira["ultimos_contatos"][0]["funcionario"] == "Ana Atendente"


@pytest.mark.django_db
def test_queries_evolucao_saldo_contas():
    cli = ClienteFactory()
    conta = ContaBancariaFactory(cliente=cli)
    s1 = SaldoHistoricoFactory(conta=conta, data_saldo=date(2026, 6, 1), saldo=Decimal("1000.00"))
    s2 = SaldoHistoricoFactory(conta=conta, data_saldo=date(2026, 7, 1), saldo=Decimal("2000.00"))

    evolucao = queries.evolucao_saldo_contas(cli.id)
    assert len(evolucao) == 2
    assert evolucao[0].data_saldo == date(2026, 7, 1)


@pytest.mark.django_db
def test_queries_produtividade_contatos():
    f1 = FuncionarioFactory(nome="Consultor Alpha")
    f2 = FuncionarioFactory(nome="Consultor Beta")
    forma = FormaContatoFactory()
    a1 = AssuntoFactory(nome="Aporte")
    a2 = AssuntoFactory(nome="Resgate")

    cli = ClienteFactory()
    ContatoFactory(cliente=cli, funcionario=f1, forma=forma, assunto=a1, data_contato=date(2026, 8, 1))
    ContatoFactory(cliente=cli, funcionario=f1, forma=forma, assunto=a2, data_contato=date(2026, 8, 2))
    ContatoFactory(cliente=cli, funcionario=f2, forma=forma, assunto=a1, data_contato=date(2026, 8, 3))

    res = queries.produtividade_contatos()
    assert res["total_atendimentos"] == 3
    assert res["por_funcionario"][0]["funcionario__nome"] == "Consultor Alpha"
    assert res["por_funcionario"][0]["total"] == 2

    # Com filtro de data
    res_filtrado = queries.produtividade_contatos(data_inicio=date(2026, 8, 2), data_fim=date(2026, 8, 2))
    assert res_filtrado["total_atendimentos"] == 1


@pytest.mark.django_db
def test_queries_clientes_inativos():
    cli_ativo = ClienteFactory()
    cli_inativo = ClienteFactory()
    cli_sem_contato = ClienteFactory()

    func = FuncionarioFactory()
    forma = FormaContatoFactory()
    assunto = AssuntoFactory()

    # Contato recente (10 dias atrás)
    ContatoFactory(cliente=cli_ativo, funcionario=func, forma=forma, assunto=assunto, data_contato=date.today() - timedelta(days=10))
    # Contato antigo (45 dias atrás)
    ContatoFactory(cliente=cli_inativo, funcionario=func, forma=forma, assunto=assunto, data_contato=date.today() - timedelta(days=45))

    inativos = queries.clientes_inativos(dias=30)
    inativos_ids = [c.id for c in inativos]
    assert cli_inativo.id in inativos_ids
    assert cli_sem_contato.id in inativos_ids
    assert cli_ativo.id not in inativos_ids


@pytest.mark.django_db
def test_queries_painel_qualidade_dados():
    cli = ClienteFactory()
    ContatoQuarentena.objects.create(
        linha_origem={"cpf": "000"},
        motivo="CPF_INVALIDO",
        detalhe="Invalido",
        resolvido=False
    )
    ContatoQuarentena.objects.create(
        linha_origem={"cpf": "111"},
        motivo="CLIENTE_INEXISTENTE",
        detalhe="Orfao",
        resolvido=True
    )

    painel = queries.painel_qualidade_dados()
    assert painel["total_clientes"] >= 1
    assert painel["quarentena_pendente"] == 1
    assert painel["quarentena_resolvida"] == 1
