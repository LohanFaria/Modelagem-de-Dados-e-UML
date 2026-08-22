import sys
from django.core.management.base import BaseCommand, CommandError
from apps.importacao.services import ImportadorPlanilhasService


class Command(BaseCommand):
    help = "Importa dados das planilhas legadas (Clientes, Investimentos, Contatos) para o banco 3FN."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help="Caminho do arquivo Excel (.xlsx) de origem.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Executa a leitura e validações sem persistir alterações no banco.",
        )
        parser.add_argument(
            "--sem-validacao-cpf",
            action="store_true",
            help="Permite importação de CPFs fictícios em ambiente de teste/acadêmico.",
        )

    def handle(self, *args, **options):
        arquivo = options["arquivo"]
        dry_run = options["dry_run"]
        sem_validacao_cpf = options["sem_validacao_cpf"]

        self.stdout.write(self.style.NOTICE(f"Iniciando importação de: {arquivo}"))
        if dry_run:
            self.stdout.write(self.style.WARNING("MODO SIMULAÇÃO (--dry-run): nenhuma alteração será salva."))

        try:
            service = ImportadorPlanilhasService(arquivo, sem_validacao_cpf=sem_validacao_cpf)
            relatorio = service.executar(dry_run=dry_run)
        except Exception as e:
            raise CommandError(f"Falha na importação: {e}") from e

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("RELATÓRIO DE IMPORTAÇÃO"))
        self.stdout.write("=" * 50)
        
        c = relatorio["clientes"]
        self.stdout.write(f"• Clientes: {c['lidas']} linhas lidas | {c['clientes_criados']} novos clientes | {c['contas_criadas']} novas contas | {c['saldos_criados']} registros de saldo")
        
        i = relatorio["investimentos"]
        self.stdout.write(f"• Investimentos: {i['lidas']} linhas lidas | {i['criados']} criados | {i['ignorados']} ignorados (sem cliente)")
        
        ct = relatorio["contatos"]
        self.stdout.write(f"• Contatos: {ct['lidas']} linhas lidas | {ct['criados']} criados | {ct['quarentenados']} em quarentena")
        self.stdout.write("=" * 50 + "\n")
