from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from .permissions import mascarar_cpf_para_usuario


class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1


class SaldoHistoricoInline(admin.TabularInline):
    model = SaldoHistorico
    extra = 1
    ordering = ["-data_saldo"]


class ContaBancariaInline(admin.StackedInline):
    model = ContaBancaria
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "exibir_cpf",
        "qtd_contas",
        "saldo_consolidado_display",
        "total_investido_display",
        "criado_em",
    )
    search_fields = ("nome", "cpf")
    readonly_fields = ("criado_em", "atualizado_em")
    inlines = [TelefoneInline, EmailInline, ContaBancariaInline]

    def exibir_cpf(self, obj):
        request = getattr(self, "_current_request", None)
        return mascarar_cpf_para_usuario(obj.cpf, getattr(request, "user", None))
    exibir_cpf.short_description = "CPF"

    def qtd_contas(self, obj):
        return obj.contas.count()
    qtd_contas.short_description = "Nº Contas"

    def saldo_consolidado_display(self, obj):
        val = obj.saldo_atual_consolidado()
        return format_html("<b>R$ {}</b>", f"{val:,.2f}")
    saldo_consolidado_display.short_description = "Saldo Atual"

    def total_investido_display(self, obj):
        val = obj.total_investido()
        return format_html("<b>R$ {}</b>", f"{val:,.2f}")
    total_investido_display.short_description = "Total Investido"


    def get_queryset(self, request):
        self._current_request = request
        qs = super().get_queryset(request)
        return qs.prefetch_related("contas__saldos", "investimentos", "telefones", "emails")

    def has_delete_permission(self, request, obj=None):
        # Bloqueia exclusão de cliente para o grupo Consultor
        if request.user.groups.filter(name="Consultor").exists() and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "banco", "agencia", "conta", "saldo_atual_display")
    list_filter = ("banco",)
    search_fields = ("cliente__nome", "cliente__cpf", "conta")
    list_select_related = ("cliente",)
    inlines = [SaldoHistoricoInline]

    def saldo_atual_display(self, obj):
        return f"R$ {obj.saldo_atual():,.2f}"
    saldo_atual_display.short_description = "Saldo Atual"


@admin.register(SaldoHistorico)
class SaldoHistoricoAdmin(admin.ModelAdmin):
    list_display = ("conta", "data_saldo", "saldo")
    list_filter = ("data_saldo", "conta__banco")
    search_fields = ("conta__cliente__nome", "conta__conta")
    list_select_related = ("conta__cliente",)


@admin.register(Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    list_display = ("cliente", "numero", "tipo")
    list_filter = ("tipo",)
    search_fields = ("cliente__nome", "numero")
    list_select_related = ("cliente",)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("cliente", "endereco", "principal")
    list_filter = ("principal",)
    search_fields = ("cliente__nome", "endereco")
    list_select_related = ("cliente",)
