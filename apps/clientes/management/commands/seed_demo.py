import sys
import random
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.clientes.models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from apps.investimentos.models import TipoInvestimento, Investimento
from apps.relacionamento.models import Funcionario, FormaContato, Assunto, Contato


class Command(BaseCommand):
    help = "Popula o banco com 50 clientes fictícios para demonstração e homologação."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Força a execução mesmo se DEBUG for False (útil em testes).",
        )

    def handle(self, *args, **options):
        is_dev = getattr(settings, "DEBUG", False) or options.get("force") or "pytest" in sys.modules
        if not is_dev:
            self.stdout.write(self.style.ERROR("seed_demo só pode ser executado em ambiente de desenvolvimento/testes."))
            return

        self.stdout.write(self.style.NOTICE("Populando base de dados de demonstração..."))

        # Domínios
        tipos_nomes = ["CDB Pré-fixado", "LCI/LCA", "Tesouro Selic", "Ações B3", "Fundos Multimercado", "Previdência Privada"]
        tipos_objs = [TipoInvestimento.objects.get_or_create(nome=n)[0] for n in tipos_nomes]

        formas_nomes = ["WhatsApp", "Telefone", "E-mail", "Presencial"]
        formas_objs = [FormaContato.objects.get_or_create(nome=n)[0] for n in formas_nomes]

        assuntos_nomes = ["Abertura de Conta", "Revisão de Carteira", "Resgate de Aplicação", "Aporte Adicional", "Rentabilidade Mensal"]
        assuntos_objs = [Assunto.objects.get_or_create(nome=n)[0] for n in assuntos_nomes]

        funcs_nomes = ["Carlos Mendes", "Fernanda Lima", "Roberto Alves", "Juliana Santos", "Marcelo Oliveira"]
        funcs_objs = [Funcionario.objects.get_or_create(nome=n, defaults={"matricula": f"FUNC-{i:03d}"})[0] for i, n in enumerate(funcs_nomes, 1)]

        bancos = ["Banco XPTO", "Banco do Brasil", "Itaú", "Bradesco", "Santander", "BTG Pactual"]

        for i in range(1, 51):
            cpf_num = f"{i:03d}.{i:03d}.{i:03d}-{i%100:02d}"
            cliente, _ = Cliente.objects.get_or_create(
                cpf=cpf_num,
                defaults={"nome": f"Cliente Demonstração {i}"}
            )

            # Telefones
            Telefone.objects.get_or_create(
                cliente=cliente,
                numero=f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                tipo="CELULAR"
            )

            # Email
            Email.objects.get_or_create(
                cliente=cliente,
                endereco=f"cliente{i}@demo.xpto.com.br",
                principal=True
            )

            # Conta Bancária
            conta, _ = ContaBancaria.objects.get_or_create(
                cliente=cliente,
                banco=random.choice(bancos),
                agencia=f"{random.randint(1000, 9999)}",
                conta=f"{random.randint(10000, 99999)}-{random.randint(0, 9)}"
            )

            # Saldos Históricos (últimos 3 meses)
            for m in range(3):
                data_s = date.today() - timedelta(days=m * 30)
                SaldoHistorico.objects.get_or_create(
                    conta=conta,
                    data_saldo=data_s,
                    defaults={"saldo": Decimal(f"{random.randint(5000, 150000)}.{random.randint(0, 99):02d}")}
                )

            # Investimentos
            Investimento.objects.get_or_create(
                cliente=cliente,
                tipo=random.choice(tipos_objs),
                defaults={
                    "valor_investido": Decimal(f"{random.randint(10000, 300000)}.{random.randint(0, 99):02d}"),
                    "data_aplicacao": date.today() - timedelta(days=random.randint(10, 365))
                }
            )

            # Contatos
            Contato.objects.get_or_create(
                cliente=cliente,
                funcionario=random.choice(funcs_objs),
                forma=random.choice(formas_objs),
                assunto=random.choice(assuntos_objs),
                data_contato=date.today() - timedelta(days=random.randint(1, 60)),
                defaults={"observacao": f"Atendimento demonstrativo de acompanhamento #{i}."}
            )

        self.stdout.write(self.style.SUCCESS("Base de demonstração populada com 50 clientes com sucesso!"))
