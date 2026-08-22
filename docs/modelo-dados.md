# Modelo de Dados em 3FN — Sistema XPTO Investimentos

## Diagrama Entidade-Relacionamento (Mermaid)

```mermaid
erDiagram
    Cliente ||--o{ Telefone : "possui"
    Cliente ||--o{ Email : "possui"
    Cliente ||--o{ ContaBancaria : "possui"
    ContaBancaria ||--o{ SaldoHistorico : "registra"
    Cliente ||--o{ Investimento : "aplica"
    TipoInvestimento ||--o{ Investimento : "categoriza"
    Cliente ||--o{ Contato : "participa"
    Funcionario ||--o{ Contato : "realiza"
    FormaContato ||--o{ Contato : "utiliza"
    Assunto ||--o{ Contato : "trata"

    Cliente {
        bigint id PK
        varchar nome
        varchar cpf UK "000.000.000-00"
        timestamp criado_em
        timestamp atualizado_em
    }

    Telefone {
        bigint id PK
        bigint cliente_id FK
        varchar numero
        varchar tipo "CELULAR/FIXO/COMERCIAL/OUTRO"
    }

    Email {
        bigint id PK
        bigint cliente_id FK
        varchar endereco
        boolean principal
    }

    ContaBancaria {
        bigint id PK
        bigint cliente_id FK
        varchar banco
        varchar agencia
        varchar conta
        timestamp criada_em
    }

    SaldoHistorico {
        bigint id PK
        bigint conta_id FK
        date data_saldo
        decimal saldo
        timestamp registrado_em
    }

    TipoInvestimento {
        bigint id PK
        varchar nome UK
        text descricao
    }

    Investimento {
        bigint id PK
        bigint cliente_id FK
        bigint tipo_id FK
        decimal valor_investido
        date data_aplicacao
        timestamp criado_em
    }

    Funcionario {
        bigint id PK
        varchar nome
        varchar matricula UK
        boolean ativo
        timestamp criado_em
    }

    FormaContato {
        bigint id PK
        varchar nome UK
    }

    Assunto {
        bigint id PK
        varchar nome UK
    }

    Contato {
        bigint id PK
        bigint cliente_id FK
        bigint funcionario_id FK
        bigint forma_id FK
        bigint assunto_id FK
        date data_contato
        text observacao
        timestamp criado_em
    }

    ContatoQuarentena {
        bigint id PK
        jsonb linha_origem
        varchar motivo "CLIENTE_INEXISTENTE/CPF_INVALIDO/DADO_FALTANTE"
        text detalhe
        timestamp importado_em
        boolean resolvido
    }
```

---

## Justificativa da Normalização até a 3FN

1. **Primeira Forma Normal (1FN)**:
   - Eliminação de atributos multivalorados em uma única célula: telefones e e-mails foram extraídos para tabelas próprias (`Telefone` e `Email`), com 1 registro por linha.
   - O saldo bancário deixou de ser uma coluna fixa em cliente e passou para o histórico (`SaldoHistorico`).

2. **Segunda Forma Normal (2FN)**:
   - Todos os atributos não-chave dependem da chave primária inteira de cada entidade.

3. **Terceira Forma Normal (3FN)**:
   - Eliminação de dependências transitivas: dados de domínio (`TipoInvestimento`, `FormaContato`, `Assunto`, `Funcionario`) foram isolados em tabelas próprias referenciadas por chaves estrangeiras.
