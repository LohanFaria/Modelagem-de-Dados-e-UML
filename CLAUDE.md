# Contexto do projeto — Sistema XPTO Investimentos

## O que é
Sistema de gestão de clientes, investimentos e contatos de uma consultoria financeira. Substitui três planilhas Excel por um banco relacional em 3FN.

## Stack
Python 3.12 · Django 5.1 · PostgreSQL 16 · Docker · pytest

## Regras não negociáveis
- Modelo de dados permanece em 3FN. Não desnormalizar sem ADR.
- PK sempre substituta (id). CPF é `unique=True`, nunca PK nem FK.
- `on_delete=PROTECT` em Investimento e Contato; `CASCADE` só em Telefone, Email, ContaBancaria e SaldoHistorico.
- Nenhum segredo em código: tudo via variável de ambiente.
- Todo código novo vem com teste.
- Nomes de models, campos e verbose_name em português.
- Idioma da interface: pt-BR. TIME_ZONE = "America/Sao_Paulo".

## Estrutura
apps/clientes · apps/investimentos · apps/relacionamento · apps/importacao · apps/relatorios · config/settings/

## Como rodar
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web pytest
