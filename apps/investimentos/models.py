from django.db import models
from auditlog.registry import auditlog


class TipoInvestimento(models.Model):
    nome = models.CharField("Nome do tipo", max_length=50, unique=True)
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Tipo de investimento"
        verbose_name_plural = "Tipos de investimento"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Investimento(models.Model):
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="investimentos",
        verbose_name="Cliente",
    )
    tipo = models.ForeignKey(
        TipoInvestimento,
        on_delete=models.PROTECT,
        related_name="investimentos",
        verbose_name="Tipo de investimento",
    )
    valor_investido = models.DecimalField("Valor investido (R$)", max_digits=14, decimal_places=2)
    data_aplicacao = models.DateField("Data de aplicação", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Investimento"
        verbose_name_plural = "Investimentos"
        ordering = ["-valor_investido"]

    def __str__(self):
        return f"{self.cliente.nome} — {self.tipo.nome}: R$ {self.valor_investido:,.2f}"


auditlog.register(Investimento)
