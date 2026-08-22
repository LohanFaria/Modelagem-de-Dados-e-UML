from rest_framework import serializers
from .models import Funcionario, FormaContato, Assunto, Contato, ContatoQuarentena


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ["id", "nome", "matricula", "ativo"]


class FormaContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaContato
        fields = ["id", "nome"]


class AssuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assunto
        fields = ["id", "nome"]


class ContatoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.ReadOnlyField(source="cliente.nome")
    funcionario_nome = serializers.ReadOnlyField(source="funcionario.nome")
    forma_nome = serializers.ReadOnlyField(source="forma.nome")
    assunto_nome = serializers.ReadOnlyField(source="assunto.nome")

    class Meta:
        model = Contato
        fields = [
            "id",
            "cliente",
            "cliente_nome",
            "funcionario",
            "funcionario_nome",
            "forma",
            "forma_nome",
            "assunto",
            "assunto_nome",
            "data_contato",
            "observacao",
            "criado_em",
        ]


class ContatoQuarentenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoQuarentena
        fields = ["id", "linha_origem", "motivo", "detalhe", "importado_em", "resolvido"]
