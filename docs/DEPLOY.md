# Guia de Implantação e Operação — Sistema XPTO

## 1. Variáveis de Ambiente de Produção

Crie o arquivo `.env` no servidor de produção:

```ini
DEBUG=False
SECRET_KEY=sua-chave-secreta-extremamente-forte-e-aleatoria
DB_NAME=xpto_prod
DB_USER=xpto_app
DB_PASSWORD=senha-forte-do-banco-de-dados
DB_HOST=db.render.internal # ou host do postgres gerenciado
DB_PORT=5432
ALLOWED_HOSTS=xpto.suaempresa.com.br
CSRF_TRUSTED_ORIGINS=https://xpto.suaempresa.com.br
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

---

## 2. Inicialização do Contêiner em Produção

```bash
# Build e execução dos containers
docker compose -f docker-compose.prod.yml up -d --build

# Aplicação das migrações
docker compose exec web python manage.py migrate

# Coleta de arquivos estáticos
docker compose exec web python manage.py collectstatic --noinput

# Checagem de segurança de deploy
docker compose exec web python manage.py check --deploy
```

---

## 3. Rotina de Backup e Restauração

### Backup Diário do PostgreSQL
```bash
./scripts/backup.sh
```

### Restauração de Backup
```bash
./scripts/restore.sh backups/xpto_backup_YYYYMMDD_HHMMSS.sql.gz
```
