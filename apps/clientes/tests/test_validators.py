import pytest
from django.core.exceptions import ValidationError
from apps.clientes.validators import validar_cpf, formatar_cpf, normalizar_telefone


def test_validar_cpf_valido():
    # CPFs matematicamente válidos conhecidos
    cpfs_validos = [
        "52998224725",
        "529.982.247-25",
        "11144477735",
        "111.444.777-35",
        "00000000191",
    ]
    for cpf in cpfs_validos:
        validar_cpf(cpf)


@pytest.mark.parametrize("cpf_invalido", [
    "",
    "123",
    "1234567890",
    "123456789012",
    "abcdefghijk",
    "123.456.78a-90",
])
def test_validar_cpf_tamanho_ou_formato_invalido(cpf_invalido):
    with pytest.raises(ValidationError):
        validar_cpf(cpf_invalido)


@pytest.mark.parametrize("digito", range(10))
def test_validar_cpf_digitos_repetidos(digito):
    cpf_repetido = str(digito) * 11
    with pytest.raises(ValidationError, match="todos os dígitos repetidos"):
        validar_cpf(cpf_repetido)


@pytest.mark.parametrize("cpf_dv_invalido", [
    "11122233344",
    "52998224724",  # último dígito errado (esperado 5)
    "52998224715",  # penúltimo dígito errado (esperado 2)
    "12345678900",

])
def test_validar_cpf_digito_verificador_invalido(cpf_dv_invalido):
    with pytest.raises(ValidationError, match="dígito verificador"):
        validar_cpf(cpf_dv_invalido)


def test_formatar_cpf():
    assert formatar_cpf("52998224725") == "529.982.247-25"
    assert formatar_cpf("529.982.247-25") == "529.982.247-25"
    assert formatar_cpf("  52998224725  ") == "529.982.247-25"
    # Se comprimento não for 11, retorna o original limpo
    assert formatar_cpf("123") == "123"


def test_normalizar_telefone():
    assert normalizar_telefone("(11) 98765-4321") == "11987654321"
    assert normalizar_telefone("  (21) 3333-4444  ") == "2133334444"
    assert normalizar_telefone("+55 (11) 91234-5678") == "5511912345678"
    assert normalizar_telefone("11999998888") == "11999998888"
