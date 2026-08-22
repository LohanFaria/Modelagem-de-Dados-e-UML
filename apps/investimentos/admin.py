from django.contrib import admin
from django.utils.html import format_html
from .models import TipoInvestimento, Investimento


@admin.register(TipoInvestimento)
class TipoInvestimentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Investimento)
class InvestimentoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "tipo", "valor_investido_display", "data_aplicacao", "criado_em")
    list_filter = ("tipo", "data_aplicacao")
    search_fields = ("cliente__nome", "cliente__cpf")
    autocomplete_fields = ["cliente"]
    list_select_related = ("cliente", "tipo")

    def valor_investido_display(self, obj):
        return format_html("<b>R$ {:,.2f}</b>", obj.valor_investido)
    valor_investido_display.short_description = "Valor Investido"
