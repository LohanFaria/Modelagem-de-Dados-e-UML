from rest_framework import serializers
from .models import Cliente, Telefone, Email, ContaBancaria, SaldoHistorico
from .permissions import mascarar_cpf_para_usuario


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = ["id", "numero", "tipo"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["id", "endereco", "principal"]


class SaldoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaldoHistorico
        fields = ["id", "data_saldo", "saldo"]


class ContaBancariaSerializer(serializers.ModelSerializer):
    saldos = SaldoHistoricoSerializer(many=True, read_only=True)
    saldo_atual = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = ContaBancaria
        fields = ["id", "banco", "agencia", "conta", "saldo_atual", "saldos"]


class ClienteSerializer(serializers.ModelSerializer):
    telefones = TelefoneSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    contas = ContaBancariaSerializer(many=True, read_only=True)
    cpf_exibicao = serializers.SerializerMethodField()
    total_investido = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    saldo_consolidado = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nome",
            "cpf",
            "cpf_exibicao",
            "saldo_consolidado",
            "total_investido",
            "telefones",
            "emails",
            "contas",
            "criado_em",
            "atualizado_em",
        ]

    def get_cpf_exibicao(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        return mascarar_cpf_para_usuario(obj.cpf, user)

    def get_saldo_consolidado(self, obj):
        return obj.saldo_atual_consolidado()
