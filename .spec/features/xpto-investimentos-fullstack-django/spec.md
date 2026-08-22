# Spec: XPTO Investimentos Full-Stack Django

> feature: xpto-investimentos-fullstack-django
> status: auditada


## Contexto

Sistema web transacional com banco de dados relacional normalizado em 3FN (Django 5 + PostgreSQL 16) para gestão de clientes, investimentos e histórico de relacionamentos da XPTO Investimentos, substituindo planilhas legadas com migração idempotente, auditoria e relatórios.

## Histórias

### US-001 — Fundação e Ambiente de Desenvolvimento

Como desenvolvedor e arquiteto, quero uma infraestrutura containerizada e modular com Django 5.1 e PostgreSQL 16, para que o sistema possa ser executado e testado de forma reprodutível e segura.

#### AC-001 — Ambiente de desenvolvimento executável via Docker

- **Dado** um ambiente de desenvolvimento limpo com Docker
- **Quando** o comando de inicialização dos containers for executado
- **Então** os serviços de banco de dados PostgreSQL e aplicação Django iniciam com status saudável
- **E** a página administrativa inicial responde na porta local configurada sem erros críticos de checagem

---

### US-002 — Modelo de Dados Normalizado em 3FN e Integridade Relacional

Como analista de dados e gestor de operações, quero que as informações de clientes, investimentos e contatos sigam rigorosamente a Terceira Forma Normal (3FN), para que não haja duplicação de dados nem perda de integridade relacional.

#### AC-002 — Unicidade de CPF e dados de contato atômicos

- **Dado** um cliente já cadastrado com determinado CPF
- **Quando** houver tentativa de inserção de outro cliente com o mesmo CPF
- **Então** a operação é rejeitada com aviso de duplicidade
- **E** telefones e e-mails são armazenados em tabelas filhas dedicadas com cardinalidade N:1

#### AC-003 — Unicidade temporal de saldo por conta bancária

- **Dado** uma conta bancária com registro de saldo histórico em determinada data
- **Quando** houver tentativa de registrar um novo saldo para a mesma conta na mesma data
- **Então** a gravação é rejeitada por violação de unicidade composta (conta + data)

#### AC-004 — Proteção referencial em cascata e bloqueio de exclusão

- **Dado** um cliente cadastrado com investimentos ou contatos vinculados
- **Quando** for solicitada a exclusão do cliente
- **Então** a exclusão é bloqueada impedindo a perda de dados transacionais
- **E** para clientes sem vínculos transacionais, seus telefones, e-mails e contas são removidos em cascata

#### AC-005 — Validação de formato e dígitos verificadores de CPF

- **Dado** uma entrada de dados com CPF inválido no cálculo dos dígitos verificadores
- **Quando** o validador for acionado na gravação do registro
- **Então** o formulário rejeita a gravação com mensagem de erro amigável

---

### US-003 — Interface Administrativa e Gestão Operacional

Como consultor ou gestor operacional, quero uma interface administrativa em português para gerenciar clientes e seus vínculos em uma visão unificada, para que o cadastro seja ágil e sem complexidade técnica.

#### AC-006 — Cadastro unificado de cliente com blocos inline

- **Dado** um operador autenticado no painel administrativo
- **Quando** ele acessa a tela de edição ou criação de um cliente
- **Então** consegue incluir telefones, e-mails e contas bancárias na mesma página através de formulários integrados

#### AC-007 — Visualização de indicadores consolidados e busca rápida

- **Dado** a listagem geral de clientes no painel administrativo
- **Quando** o operador visualiza a tabela ou realiza busca por nome ou CPF
- **Então** a tela exibe o saldo atual consolidado e total investido de cada cliente
- **E** a página é carregada sem degradação por consultas repetitivas ao banco

---

### US-004 — Controle de Acesso, Papéis e Trilha de Auditoria

Como responsável por segurança e conformidade com a LGPD, quero que o acesso seja restrito a perfis específicos (Consultor, Gestor, Auditor) e que alterações financeiras fiquem registradas, para garantir rastreabilidade e sigilo de dados sensíveis.

#### AC-008 — Restrições de permissão e mascaramento de dados para consultores

- **Dado** um usuário pertencente ao grupo Consultor
- **Quando** ele visualiza a listagem de clientes ou tenta excluir um cadastro
- **Então** os números de CPF são exibidos com dígitos centrais mascarados
- **E** a ação de exclusão é negada com aviso de falta de permissão

#### AC-009 — Trilha de auditoria automática em dados financeiros

- **Dado** uma alteração em registro de cliente, conta bancária, saldo ou investimento
- **Quando** a alteração é salva no sistema
- **Então** um registro de auditoria é gravado contendo o usuário responsável, data/hora e valores anteriores e novos

---

### US-005 — Importação e Migração Idempotente das Planilhas Legadas

Como gestor de migração, quero importar as três planilhas legadas (Clientes, Investimentos, Contatos) tratando redundâncias e dados inválidos, para que 100% dos dados sejam migrados ou quarentenados sem perda de informação.

#### AC-010 — Deduplicação e quebra de campos multivalorados na carga

- **Dado** um arquivo de planilha contendo múltiplos registros para o mesmo cliente e células com múltiplos telefones
- **Quando** o comando de importação for executado
- **Então** é criado apenas um registro de cliente com múltiplas contas e telefones individuais separados
- **E** a execução repetida do comando não gera duplicatas no banco de dados

#### AC-011 — Quarentena de contatos órfãos e dados divergentes

- **Dado** uma linha na planilha de contatos cujo CPF não exista na base de clientes
- **Quando** a rotina de importação processa o arquivo
- **Então** a linha bruta é preservada em tabela de quarentena com o motivo registrado
- **E** as demais linhas válidas da planilha são importadas normalmente

#### AC-012 — Modo de simulação sem alteração de banco

- **Dado** o comando de importação executado com a opção de simulação (--dry-run)
- **Quando** a leitura das planilhas é finalizada
- **Então** o relatório de total de linhas lidas, criadas e quarentenadas é exibido
- **E** nenhuma alteração é persistida no banco de dados

---

### US-006 — Consultas Analíticas e Relatórios Gerenciais

Como diretor e gestor de investimentos, quero relatórios consolidados de carteira, saldos, distribuição de investimentos e produtividade, para tomar decisões estratégicas com números confiáveis.

#### AC-013 — Geração de relatórios gerenciais consolidados via banco

- **Dado** um usuário com permissão de Gestor autenticado
- **Quando** ele acessa o módulo de relatórios (carteira, total por tipo, evolução de saldo, produtividade)
- **Então** os dados consolidados são calculados via agregações diretas do banco de dados e apresentados em tabelas formatadas em pt-BR

#### AC-014 — Bloqueio de acesso a relatórios financeiros consolidados

- **Dado** um usuário pertencente ao grupo Consultor
- **Quando** ele tenta acessar a visualização de relatórios financeiros consolidados
- **Então** o acesso é negado com aviso de privilégios insuficientes

---

### US-007 — Qualidade de Código, Cobertura de Testes e Seed de Demonstração

Como líder técnico, quero suíte de testes com cobertura mínima de 70% e gerador de dados para testes, para que o sistema seja confiável e fácil de homologar.

#### AC-015 — Cobertura de testes automatizados e validação de regressão

- **Dado** a suíte de testes automatizados do projeto
- **Quando** o comando de testes for executado com medição de cobertura
- **Então** a cobertura total de código alcança no mínimo 70%
- **E** todos os cenários de restrições de integridade, validadores e importação passam com sucesso

#### AC-016 — Geração de dados de demonstração coerentes

- **Dado** um ambiente de desenvolvimento local
- **Quando** o comando de população de demonstração for executado
- **Então** uma base com clientes, investimentos e contatos fictícios estruturados é criada rapidamente para validação manual

## Fora de escopo

- Aplicativo móvel para clientes finais.
- Portal web de autoatendimento para clientes.
- Integração em tempo real com sistemas da B3 ou Open Finance.
- Cálculo de marcação a mercado ou rentabilidade diária automatizada.
- Arquitetura multi-tenant (múltiplas empresas no mesmo banco).

## Suposições

| ID | Suposição | Status | Resolução |
|---|---|---|---|
| ASM-001 | A base de dados oficial e homologada para persistência é o PostgreSQL 16. | confirmada | Definido em ADR-01 da especificação técnica. |
| ASM-002 | A interface primária de operação na versão 1.0 é o Django Admin customizado com views adicionais para relatórios. | confirmada | Definido em ADR-02 e Seção 2 da especificação técnica. |
| ASM-003 | Os CPFs fictícios presentes no arquivo Excel do exercício acadêmico requerem uma flag `--sem-validacao-cpf` para permitir a carga de testes. | confirmada | Registrado na seção 6.4 e 9.4 da especificação técnica. |
| ASM-004 | A stack de testes automatizados utiliza `pytest`, `pytest-django` e `factory-boy`. | confirmada | Configurado nas dependências e requirements. |

## Perguntas em aberto

| ID | Pergunta | Status | Resposta |
|---|---|---|---|
| Q-001 | O relatório analítico de carteira deve ter opção futura de exportação direta para formato PDF ou XLSX? | respondida | Sim, planejado para a Fase 8 (evoluções opcionais pós-v1.0 estável). |
