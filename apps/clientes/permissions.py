import re


def mascarar_cpf(cpf: str) -> str:
    """Mascara os dígitos centrais do CPF: 111.***.***-44"""
    if not cpf:
        return ""
    n = re.sub(r"\D", "", cpf)
    if len(n) == 11:
        return f"{n[:3]}.***.***-{n[9:]}"
    return cpf


def mascarar_cpf_para_usuario(cpf: str, user) -> str:
    """Retorna CPF mascarado se o usuário for do grupo Consultor (ou sem privilégio)."""
    if not user:
        return mascarar_cpf(cpf)
    if user.is_superuser:
        return cpf
    if user.groups.filter(name__in=["Gestor", "Auditor"]).exists():
        return cpf
    if user.groups.filter(name="Consultor").exists():
        return mascarar_cpf(cpf)
    return mascarar_cpf(cpf)
