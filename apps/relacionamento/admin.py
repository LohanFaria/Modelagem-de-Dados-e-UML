from django.contrib import admin
from .models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("nome", "matricula")


@admin.register(FormaContato)
class FormaContatoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "funcionario", "forma", "assunto", "data_contato")
    list_filter = ("funcionario", "forma", "assunto")
    date_hierarchy = "data_contato"
    search_fields = ("cliente__nome", "cliente__cpf", "observacao")
    autocomplete_fields = ["cliente"]
    list_select_related = ("cliente", "funcionario", "forma", "assunto")


@admin.register(ContatoQuarentena)
class ContatoQuarentenaAdmin(admin.ModelAdmin):
    list_display = ("importado_em", "motivo", "detalhe", "resolvido")
    list_filter = ("motivo", "resolvido")
    readonly_fields = ("linha_origem", "importado_em")
    actions = ["marcar_como_resolvido"]

    def marcar_como_resolvido(self, request, queryset):
        queryset.update(resolvido=True)
    marcar_como_resolvido.short_description = "Marcar selecionados como resolvido"
