from django.db import models
from django.db.models import Max
from auditlog.registry import auditlog
from .validators import validar_cpf, formatar_cpf


class Cliente(models.Model):
    nome = models.CharField("Nome completo", max_length=150)
    cpf = models.CharField(
        "CPF",
        max_length=14,
        unique=True,
        validators=[validar_cpf],
        help_text="Formato: 000.000.000-00",
    )
    criado_em = models.DateTimeField("Cadastrado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

    def clean(self):
        super().clean()
        if self.cpf:
            self.cpf = formatar_cpf(self.cpf)

    def total_investido(self):
        """Soma de todos os investimentos ativos do cliente."""
        return sum(inv.valor_investido for inv in self.investimentos.all())

    def saldo_atual_consolidado(self):
        """Soma do saldo mais recente de cada conta bancária do cliente."""
        total = 0
        for conta in self.contas.all():
            ultimo_saldo = conta.saldos.order_by("-data_saldo").first()
            if ultimo_saldo:
                total += ultimo_saldo.saldo
        return total


class Telefone(models.Model):
    TIPOS = [
        ("CELULAR", "Celular"),
        ("FIXO", "Fixo"),
        ("COMERCIAL", "Comercial"),
        ("OUTRO", "Outro"),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="telefones")
    numero = models.CharField("Número", max_length=20)
    tipo = models.CharField("Tipo", max_length=10, choices=TIPOS, default="CELULAR")

    class Meta:
        verbose_name = "Telefone"
        verbose_name_plural = "Telefones"

    def __str__(self):
        return f"{self.numero} ({self.get_tipo_display()})"


class Email(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="emails")
    endereco = models.EmailField("E-mail")
    principal = models.BooleanField("Principal?", default=False)

    class Meta:
        verbose_name = "E-mail"
        verbose_name_plural = "E-mails"

    def __str__(self):
        return self.endereco


class ContaBancaria(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="contas")
    banco = models.CharField("Banco", max_length=60)
    agencia = models.CharField("Agência", max_length=10)
    conta = models.CharField("Conta", max_length=20)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conta bancária"
        verbose_name_plural = "Contas bancárias"
        constraints = [
            models.UniqueConstraint(
                fields=["banco", "agencia", "conta"],
                name="unique_banco_agencia_conta"
            )
        ]

    def __str__(self):
        return f"{self.banco} Ag {self.agencia} Cc {self.conta}"

    def saldo_atual(self):
        ultimo = self.saldos.order_by("-data_saldo").first()
        return ultimo.saldo if ultimo else 0


class SaldoHistorico(models.Model):
    conta = models.ForeignKey(ContaBancaria, on_delete=models.CASCADE, related_name="saldos")
    data_saldo = models.DateField("Data do saldo")
    saldo = models.DecimalField("Saldo (R$)", max_digits=14, decimal_places=2)
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de saldo"
        verbose_name_plural = "Históricos de saldo"
        ordering = ["-data_saldo"]
        constraints = [
            models.UniqueConstraint(
                fields=["conta", "data_saldo"],
                name="unique_conta_data_saldo"
            )
        ]

    def __str__(self):
        dt_str = self.data_saldo.strftime("%d/%m/%Y") if hasattr(self.data_saldo, "strftime") else str(self.data_saldo)
        return f"{self.conta} — R$ {self.saldo:,.2f} em {dt_str}"



auditlog.register(Cliente)
auditlog.register(ContaBancaria)
auditlog.register(SaldoHistorico)
