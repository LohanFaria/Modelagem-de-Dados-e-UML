from django.db import models
from auditlog.registry import auditlog


class Funcionario(models.Model):
    nome = models.CharField("Nome do funcionário", max_length=100)
    matricula = models.CharField("Matrícula", max_length=20, unique=True, null=True, blank=True)
    ativo = models.BooleanField("Ativo?", default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class FormaContato(models.Model):
    nome = models.CharField("Forma de contato", max_length=30, unique=True)

    class Meta:
        verbose_name = "Forma de contato"
        verbose_name_plural = "Formas de contato"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Assunto(models.Model):
    nome = models.CharField("Assunto / Produto", max_length=60, unique=True)

    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Contato(models.Model):
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="contatos",
        verbose_name="Cliente",
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="contatos",
        verbose_name="Funcionário",
    )
    forma = models.ForeignKey(
        FormaContato,
        on_delete=models.PROTECT,
        verbose_name="Forma de contato",
    )
    assunto = models.ForeignKey(
        Assunto,
        on_delete=models.PROTECT,
        verbose_name="Assunto",
    )
    data_contato = models.DateField("Data do contato")
    observacao = models.TextField("Observação", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ["-data_contato"]
        indexes = [
            models.Index(fields=["cliente", "-data_contato"]),
        ]

    def __str__(self):
        return f"{self.cliente.nome} — {self.assunto.nome} ({self.data_contato:%d/%m/%Y})"


class ContatoQuarentena(models.Model):
    """Linhas de contato que não puderam ser vinculadas a um cliente existente."""
    MOTIVOS = [
        ("CLIENTE_INEXISTENTE", "CPF não encontrado na base de clientes"),
        ("CPF_INVALIDO", "CPF com dígito verificador inválido"),
        ("DADO_FALTANTE", "Campo obrigatório ausente"),
    ]
    linha_origem = models.JSONField("Linha bruta da planilha")
    motivo = models.CharField("Motivo", max_length=30, choices=MOTIVOS)
    detalhe = models.TextField("Detalhe do problema", blank=True)
    importado_em = models.DateTimeField("Importado em", auto_now_add=True)
    resolvido = models.BooleanField("Resolvido?", default=False)

    class Meta:
        verbose_name = "Contato em quarentena"
        verbose_name_plural = "Contatos em quarentena"
        ordering = ["-importado_em"]

    def __str__(self):
        return f"Quarentena ({self.get_motivo_display()}) — {self.importado_em:%d/%m/%Y %H:%M}"


auditlog.register(Contato)
