from __future__ import annotations
import re
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from apps.clientes.validators import formatar_cpf


def parse_cpf(valor: str) -> str:
    """Normaliza e aplica máscara ao CPF."""
    if not valor:
        return ""
    n = re.sub(r"\D", "", str(valor))
    if len(n) == 11:
        return formatar_cpf(n)
    return str(valor).strip()


def parse_telefones(valor: str) -> list[str]:
    """Quebra múltiplos telefones separados por /, ;, ou vírgula."""
    if not valor:
        return []
    partes = re.split(r"[/;,|]", str(valor))
    telefones = []
    for p in partes:
        p_limpo = p.strip()
        if p_limpo and p_limpo not in telefones:
            telefones.append(p_limpo)
    return telefones


def parse_emails(valor: str) -> list[str]:
    """Quebra múltiplos e-mails separados por /, ;, ou vírgula."""
    if not valor:
        return []
    partes = re.split(r"[/;,|\s]+", str(valor))
    emails = []
    for p in partes:
        p_limpo = p.strip().lower()
        if p_limpo and "@" in p_limpo and p_limpo not in emails:
            emails.append(p_limpo)
    return emails


def parse_moeda(valor) -> Decimal:
    """Converte valores monetários como 'R$ 15.000,00' ou '15000.50' para Decimal."""
    if valor is None:
        return Decimal("0.00")
    if isinstance(valor, (int, float, Decimal)):
        return Decimal(str(valor)).quantize(Decimal("0.01"))
    
    s = str(valor).strip()
    s = re.sub(r"[R$\s]", "", s)
    
    # Se houver '.' como milhar e ',' como decimal (ex: 15.000,50)
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    
    try:
        return Decimal(s).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")


def parse_data(valor) -> date | None:
    """Converte string de data dd/mm/aaaa ou datetime para date."""
    if not valor:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    
    s = str(valor).strip()
    formatos = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"]
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None
