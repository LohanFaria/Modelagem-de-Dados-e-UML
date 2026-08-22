# Plano de execução — xpto-investimentos-fullstack-django

> gerado por `onp-spec plano` em 2026-08-22 01:07 — NÃO edite à mão;
> mudou tasks.md ou a config? Regenere: `onp-spec plano xpto-investimentos-fullstack-django`

## Resumo — o que vai acontecer

- **7 tarefa(s) pendente(s)**: 7 em 7 faixa(s) paralela(s) + 0 sequencial(is)
- **1 faixa = 1 worktree + 1 branch + 1 janela de contexto limpa** — faixas não compartilham nenhum arquivo entre si
- prefere outra seleção ou uma após a outra? Regenere com `onp-spec plano xpto-investimentos-fullstack-django --paralelizar T-xxx,T-yyy` ou `--sequencial`
- tudo acontece na branch de trabalho `spec/xpto-investimentos-fullstack-django`; levar para a main é decisão sua

## Faixas e ondas

### Onda 1 — faixa-1 ∥ faixa-2 ∥ faixa-3

#### faixa-1 — branch `spec/xpto-investimentos-fullstack-django-faixa-1` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-1`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-001 | Fundação e ambiente de desenvolvimento Docker e Django | `claude-sonnet-5` | medium | `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `manage.py`, `config/settings/base.py`, `config/settings/dev.py`, `config/settings/prod.py`, `config/urls.py`, `CLAUDE.md`, `.env.example`, `.gitignore` |

#### faixa-2 — branch `spec/xpto-investimentos-fullstack-django-faixa-2` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-2`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-002 | Modelagem de dados em 3FN, validadores de CPF e constraints | `claude-sonnet-5` | medium | `apps/clientes/models.py`, `apps/clientes/validators.py`, `apps/investimentos/models.py`, `apps/relacionamento/models.py`, `apps/clientes/tests/test_models.py`, `apps/clientes/tests/test_validators.py`, `apps/investimentos/tests/test_models.py`, `apps/relacionamento/tests/test_models.py` |

#### faixa-3 — branch `spec/xpto-investimentos-fullstack-django-faixa-3` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-3`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-003 | Interface administrativa customizada com inlines e listagens consolidadas | `claude-sonnet-5` | medium | `apps/clientes/admin.py`, `apps/investimentos/admin.py`, `apps/relacionamento/admin.py`, `apps/clientes/tests/test_admin.py` |

### Onda 2 — faixa-4 ∥ faixa-5 ∥ faixa-6

#### faixa-4 — branch `spec/xpto-investimentos-fullstack-django-faixa-4` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-4`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-004 | Controle de acesso por grupos, mascaramento de CPF e auditoria | `claude-sonnet-5` | medium | `apps/clientes/permissions.py`, `apps/clientes/migrations/0002_create_groups.py`, `apps/clientes/tests/test_security.py` |

#### faixa-5 — branch `spec/xpto-investimentos-fullstack-django-faixa-5` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-5`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-005 | Módulo de importação ETL das planilhas legadas com deduplicação e quarentena | `claude-sonnet-5` | medium | `apps/importacao/parsers.py`, `apps/importacao/services.py`, `apps/importacao/management/commands/importar_planilhas.py`, `apps/importacao/tests/test_importacao.py` |

#### faixa-6 — branch `spec/xpto-investimentos-fullstack-django-faixa-6` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-6`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-006 | Consultas analíticas e views de relatórios gerenciais | `claude-sonnet-5` | medium | `apps/relatorios/queries.py`, `apps/relatorios/views.py`, `apps/relatorios/urls.py`, `apps/relatorios/templates/relatorios/base.html`, `apps/relatorios/tests/test_queries.py`, `apps/relatorios/tests/test_views.py` |

### Onda 3 — faixa-7

#### faixa-7 — branch `spec/xpto-investimentos-fullstack-django-faixa-7` — worktree `../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-7`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-007 | Factories, suíte de testes de integração e seed de demonstração | `claude-sonnet-5` | medium | `apps/clientes/factories.py`, `apps/investimentos/factories.py`, `apps/relacionamento/factories.py`, `apps/clientes/management/commands/seed_demo.py`, `tests/test_integration.py` |

## Gestão de branches e commits

1. branch de trabalho `spec/xpto-investimentos-fullstack-django` criada do ponto atual (se ainda não existir)
2. cada faixa nasce dela como branch própria e roda no seu worktree — **1 tarefa = 1 commit** (`T-xxx feature: título`)
3. terminou a onda → merge `--no-ff` de cada faixa de volta, na ordem; conflito interrompe a faixa e pede resolução humana
4. faixa mesclada → worktree removido, branch apagada, tarefa marcada `[concluida]` no tasks.md
5. gate final na branch de trabalho: `onp-spec verify xpto-investimentos-fullstack-django` + `onp-spec audit --ci` — **exit 0 ou não está pronto**

## Como executar

### ▶ Paralelo nativo no Antigravity (janelas limpas, sem Claude CLI)

1. **Prepare a branch de trabalho e os worktrees** (terminal, na raiz do repositório):

```bash
git checkout -b spec/xpto-investimentos-fullstack-django   # ou: git checkout spec/xpto-investimentos-fullstack-django
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-1 -b spec/xpto-investimentos-fullstack-django-faixa-1
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-2 -b spec/xpto-investimentos-fullstack-django-faixa-2
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-3 -b spec/xpto-investimentos-fullstack-django-faixa-3
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-4 -b spec/xpto-investimentos-fullstack-django-faixa-4
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-5 -b spec/xpto-investimentos-fullstack-django-faixa-5
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-6 -b spec/xpto-investimentos-fullstack-django-faixa-6
git worktree add ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-7 -b spec/xpto-investimentos-fullstack-django-faixa-7
```

2. **Abra um agente NOVO por faixa** (janela limpa) e cole o prompt da faixa:

#### Prompt — faixa-1

```
Você executa as tarefas da faixa-1 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-1 (branch spec/xpto-investimentos-fullstack-django-faixa-1) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-001 — "Fundação e ambiente de desenvolvimento Docker e Django"
  critérios/refs: AC-001 (Ambiente de desenvolvimento executável via Docker)
  arquivos permitidos (e seus testes): Dockerfile, docker-compose.yml, requirements.txt, manage.py, config/settings/base.py, config/settings/dev.py, config/settings/prod.py, config/urls.py, CLAUDE.md, .env.example, .gitignore
  mensagem de commit: "T-001 xpto-investimentos-fullstack-django: Fundação e ambiente de desenvolvimento Docker e Django"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-2

```
Você executa as tarefas da faixa-2 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-2 (branch spec/xpto-investimentos-fullstack-django-faixa-2) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-002 — "Modelagem de dados em 3FN, validadores de CPF e constraints"
  critérios/refs: AC-002 (Unicidade de CPF e dados de contato atômicos), AC-003 (Unicidade temporal de saldo por conta bancária), AC-004 (Proteção referencial em cascata e bloqueio de exclusão), AC-005 (Validação de formato e dígitos verificadores de CPF)
  arquivos permitidos (e seus testes): apps/clientes/models.py, apps/clientes/validators.py, apps/investimentos/models.py, apps/relacionamento/models.py, apps/clientes/tests/test_models.py, apps/clientes/tests/test_validators.py, apps/investimentos/tests/test_models.py, apps/relacionamento/tests/test_models.py
  mensagem de commit: "T-002 xpto-investimentos-fullstack-django: Modelagem de dados em 3FN, validadores de CPF e constraints"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-3

```
Você executa as tarefas da faixa-3 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-3 (branch spec/xpto-investimentos-fullstack-django-faixa-3) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-003 — "Interface administrativa customizada com inlines e listagens consolidadas"
  critérios/refs: AC-006 (Cadastro unificado de cliente com blocos inline), AC-007 (Visualização de indicadores consolidados e busca rápida)
  arquivos permitidos (e seus testes): apps/clientes/admin.py, apps/investimentos/admin.py, apps/relacionamento/admin.py, apps/clientes/tests/test_admin.py
  mensagem de commit: "T-003 xpto-investimentos-fullstack-django: Interface administrativa customizada com inlines e listagens consolidadas"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-4

```
Você executa as tarefas da faixa-4 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-4 (branch spec/xpto-investimentos-fullstack-django-faixa-4) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-004 — "Controle de acesso por grupos, mascaramento de CPF e auditoria"
  critérios/refs: AC-008 (Restrições de permissão e mascaramento de dados para consultores), AC-009 (Trilha de auditoria automática em dados financeiros)
  arquivos permitidos (e seus testes): apps/clientes/permissions.py, apps/clientes/migrations/0002_create_groups.py, apps/clientes/tests/test_security.py
  mensagem de commit: "T-004 xpto-investimentos-fullstack-django: Controle de acesso por grupos, mascaramento de CPF e auditoria"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-5

```
Você executa as tarefas da faixa-5 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-5 (branch spec/xpto-investimentos-fullstack-django-faixa-5) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-005 — "Módulo de importação ETL das planilhas legadas com deduplicação e quarentena"
  critérios/refs: AC-010 (Deduplicação e quebra de campos multivalorados na carga), AC-011 (Quarentena de contatos órfãos e dados divergentes), AC-012 (Modo de simulação sem alteração de banco)
  arquivos permitidos (e seus testes): apps/importacao/parsers.py, apps/importacao/services.py, apps/importacao/management/commands/importar_planilhas.py, apps/importacao/tests/test_importacao.py
  mensagem de commit: "T-005 xpto-investimentos-fullstack-django: Módulo de importação ETL das planilhas legadas com deduplicação e quarentena"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-6

```
Você executa as tarefas da faixa-6 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-6 (branch spec/xpto-investimentos-fullstack-django-faixa-6) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-006 — "Consultas analíticas e views de relatórios gerenciais"
  critérios/refs: AC-013 (Geração de relatórios gerenciais consolidados via banco), AC-014 (Bloqueio de acesso a relatórios financeiros consolidados)
  arquivos permitidos (e seus testes): apps/relatorios/queries.py, apps/relatorios/views.py, apps/relatorios/urls.py, apps/relatorios/templates/relatorios/base.html, apps/relatorios/tests/test_queries.py, apps/relatorios/tests/test_views.py
  mensagem de commit: "T-006 xpto-investimentos-fullstack-django: Consultas analíticas e views de relatórios gerenciais"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

#### Prompt — faixa-7

```
Você executa as tarefas da faixa-7 da feature "xpto-investimentos-fullstack-django" (fluxo onp-spec, spec-anchored).
Trabalhe SOMENTE dentro do worktree ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-7 (branch spec/xpto-investimentos-fullstack-django-faixa-7) — já preparado.
Leia primeiro: .spec/features/xpto-investimentos-fullstack-django/spec.md, .spec/features/xpto-investimentos-fullstack-django/tasks.md e .spec/constituicao.md.

Execute NESTA ORDEM (1 tarefa = 1 commit):
T-007 — "Factories, suíte de testes de integração e seed de demonstração"
  critérios/refs: AC-015 (Cobertura de testes automatizados e validação de regressão), AC-016 (Geração de dados de demonstração coerentes)
  arquivos permitidos (e seus testes): apps/clientes/factories.py, apps/investimentos/factories.py, apps/relacionamento/factories.py, apps/clientes/management/commands/seed_demo.py, tests/test_integration.py
  mensagem de commit: "T-007 xpto-investimentos-fullstack-django: Factories, suíte de testes de integração e seed de demonstração"

Regras inegociáveis:
- Todo critério de aceite referenciado vira teste com @spec:AC-xxx no título.
- NUNCA enfraqueça, pule (skip/todo) ou apague um teste para passar — teste pulado não é prova e o audit acusa.
- Rode os testes localmente com `pytest --tap` até passarem.
- NÃO edite tasks.md, NÃO rode onp-spec verify/audit e NÃO toque em outras tarefas — o orquestrador cuida disso.
- Ao final de CADA tarefa: `git add` só no que você tocou e um commit próprio.
Quando a última tarefa estiver commitada, PARE e informe o resultado — a mesclagem é do orquestrador.
```

3. **Todas terminaram? Mescle na ordem e marque as tarefas** (na árvore principal):

```bash
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-1 -m "merge faixa-1 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-1 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-1
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-001 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-2 -m "merge faixa-2 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-2 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-2
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-002 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-3 -m "merge faixa-3 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-3 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-3
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-003 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-4 -m "merge faixa-4 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-4 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-4
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-004 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-5 -m "merge faixa-5 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-5 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-5
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-005 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-6 -m "merge faixa-6 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-6 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-6
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-006 concluida
git merge --no-ff spec/xpto-investimentos-fullstack-django-faixa-7 -m "merge faixa-7 (xpto-investimentos-fullstack-django)"
git worktree remove ../onp-worktrees/Modelagem de Dados e UML-xpto-investimentos-fullstack-django-faixa-7 && git branch -d spec/xpto-investimentos-fullstack-django-faixa-7
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec tarefa xpto-investimentos-fullstack-django T-007 concluida
```

5. **Gate final** (exit 0 ou não está pronto):

```bash
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec verify xpto-investimentos-fullstack-django
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec audit --ci
```

6. **Acompanhamento (a cada ~1 min, enquanto os agentes trabalham)**: avise ANTES
   de despachar os agentes que o trabalho roda em background e que o resumo
   completo vem ao final. Marque cada tarefa no ledger quando um agente começa
   e quando termina (é disso que a tabela é feita):

```bash
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec evento --run Modelagem de Dados e UML-xpto-investimentos-fullstack-django-mt3ohy5f --tipo tarefa --tarefa <T-xxx> --faixa <faixa-N> --estado executando
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec evento --run Modelagem de Dados e UML-xpto-investimentos-fullstack-django-mt3ohy5f --tipo tarefa --tarefa <T-xxx> --faixa <faixa-N> --estado concluida
```

   E a cada ~1 min poste no chat a TABELA de andamento + um parágrafo curto,
   registrando o texto no ledger:

```bash
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec resumo xpto-investimentos-fullstack-django --tabela   # a tabela — cole no chat
node /Users/lohancoelho/.npm/_npx/f7ffc4ee4c8cdde9/node_modules/.bin/onp-spec resumo xpto-investimentos-fullstack-django --gravar --origem ia --texto "<2 a 4 frases do que está rolando>"
```

