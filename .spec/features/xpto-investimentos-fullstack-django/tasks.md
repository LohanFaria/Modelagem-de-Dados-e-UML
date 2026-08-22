# Tasks: XPTO Investimentos Full-Stack Django

> feature: xpto-investimentos-fullstack-django

## T-001 — Fundação e ambiente de desenvolvimento Docker e Django [concluida]

- Refs: US-001, AC-001
- Arquivos: Dockerfile, docker-compose.yml, requirements.txt, manage.py, config/__init__.py, config/wsgi.py, config/settings/__init__.py, config/settings/base.py, config/settings/dev.py, config/settings/prod.py, config/urls.py, CLAUDE.md, .env.example, .gitignore, apps/__init__.py, docs/DEPLOY.md, scripts/backup.sh, scripts/restore.sh, .github/workflows/ci.yml

- Notas: Configuração de settings modulares lendo variáveis de ambiente e docker-compose com Postgres 16.

## T-002 — Modelagem de dados em 3FN, validadores de CPF e constraints [concluida]

- Refs: US-002, AC-002, AC-003, AC-004, AC-005
- Arquivos: apps/clientes/__init__.py, apps/clientes/apps.py, apps/clientes/models.py, apps/clientes/validators.py, apps/clientes/migrations/__init__.py, apps/clientes/migrations/0001_initial.py, apps/investimentos/__init__.py, apps/investimentos/apps.py, apps/investimentos/models.py, apps/investimentos/migrations/__init__.py, apps/investimentos/migrations/0001_initial.py, apps/relacionamento/__init__.py, apps/relacionamento/apps.py, apps/relacionamento/models.py, apps/relacionamento/migrations/__init__.py, apps/relacionamento/migrations/0001_initial.py, apps/clientes/tests/test_models.py, apps/clientes/tests/test_validators.py, apps/investimentos/tests/test_models.py, apps/relacionamento/tests/test_models.py, docs/modelo-dados.md
- Notas: Implementar as 11 entidades de domínio + quarentena, validador de CPF, chaves substitutas, CASCADE nos dependentes e PROTECT em transações.

## T-003 — Interface administrativa customizada com inlines e listagens consolidadas [concluida]

- Refs: US-003, AC-006, AC-007
- Arquivos: apps/clientes/admin.py, apps/investimentos/admin.py, apps/relacionamento/admin.py, apps/clientes/tests/test_admin.py
- Notas: ClienteAdmin com inlines (Telefone, Email, ContaBancaria), ContaBancariaAdmin com SaldoHistorico inline, list_select_related para mitigar N+1 e colunas calculadas.

## T-004 — Controle de acesso por grupos, mascaramento de CPF e auditoria [concluida]

- Refs: US-004, AC-008, AC-009
- Arquivos: apps/clientes/permissions.py, apps/clientes/migrations/0002_create_groups.py, apps/clientes/tests/test_security.py
- Notas: Grupos Consultor, Gestor e Auditor provisionados via data migration; mascaramento de CPF para Consultor; django-auditlog integrado nos models.

## T-005 — Módulo de importação ETL das planilhas legadas com deduplicação e quarentena [concluida]

- Refs: US-005, AC-010, AC-011, AC-012
- Arquivos: apps/importacao/__init__.py, apps/importacao/apps.py, apps/importacao/parsers.py, apps/importacao/services.py, apps/importacao/management/commands/importar_planilhas.py, apps/importacao/tests/test_importacao.py
- Notas: Comando de importação com parsers de CPF/telefone/moeda/data, split de multivalorados, quarentena de órfãos e suporte a --dry-run e --sem-validacao-cpf.

## T-006 — Consultas analíticas e views de relatórios gerenciais [concluida]

- Refs: US-006, AC-013, AC-014
- Arquivos: apps/relatorios/__init__.py, apps/relatorios/apps.py, apps/relatorios/queries.py, apps/relatorios/views.py, apps/relatorios/urls.py, apps/relatorios/templates/relatorios/base.html, apps/relatorios/templates/relatorios/painel.html, apps/relatorios/templates/relatorios/carteira.html, apps/relatorios/templates/relatorios/investimentos_tipo.html, apps/relatorios/templates/relatorios/evolucao_saldo.html, apps/relatorios/templates/relatorios/produtividade.html, apps/relatorios/templates/relatorios/reativacao.html, apps/relatorios/templates/relatorios/qualidade_dados.html, apps/relatorios/tests/test_queries.py, apps/relatorios/tests/test_views.py
- Notas: Implementar queries.py com agregações ORM (Subquery/OuterRef para saldo atual) e views com restrição por permissão.

## T-007 — Factories, suíte de testes de integração e seed de demonstração [concluida]

- Refs: US-007, AC-015, AC-016
- Arquivos: apps/clientes/factories.py, apps/investimentos/factories.py, apps/relacionamento/factories.py, apps/clientes/management/commands/seed_demo.py, tests/test_integration.py, tests/test_spec_xpto_investimentos_fullstack_django.py, pytest.ini
- Notas: Configuração de factory-boy para geração de dados em testes, comando seed_demo para popular ambiente de homologação e validação de cobertura.
