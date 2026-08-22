#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
mkdir -p "${BACKUP_DIR}"

DATA=$(date +"%Y%m%d_%H%M%S")
ARQUIVO="${BACKUP_DIR}/xpto_backup_${DATA}.sql.gz"

echo "Iniciando backup do banco de dados XPTO..."

docker compose exec -T db pg_dump -U "${DB_USER:-xpto}" "${DB_NAME:-xpto}" | gzip > "${ARQUIVO}"

echo "Backup concluído com sucesso: ${ARQUIVO}"
