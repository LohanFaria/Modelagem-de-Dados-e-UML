import re
from django.core.exceptions import ValidationError


def validar_cpf(valor: str) -> None:
    """Valida CPF verificando formato e os dois dígitos verificadores."""
    numeros = re.sub(r"\D", "", valor or "")
    if len(numeros) != 11:
        raise ValidationError("CPF deve conter 11 dígitos.")
    if numeros == numeros[0] * 11:
        raise ValidationError("CPF inválido (todos os dígitos repetidos).")
    
    for i in (9, 10):
        soma = sum(int(numeros[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(numeros[i]):
            raise ValidationError("CPF inválido (dígito verificador incorreto).")


def formatar_cpf(valor: str) -> str:
    """Aplica a máscara 000.000.000-00 a um CPF de 11 dígitos numéricos."""
    n = re.sub(r"\D", "", valor or "")
    if len(n) == 11:
        return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"
    return valor or ""


def normalizar_telefone(valor: str) -> str:
    """Limpa caracteres não numéricos e formata telefone."""
    n = re.sub(r"\D", "", valor or "")
    return n
