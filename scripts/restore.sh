#!/usr/bin/env bash
set -euo pipefail

if [ -z "${1:-}" ]; then
    echo "Uso: $0 <caminho_do_backup.sql.gz>"
    exit 1
fi

ARQUIVO="$1"

if [ ! -f "${ARQUIVO}" ]; then
    echo "Arquivo de backup não encontrado: ${ARQUIVO}"
    exit 1
fi

echo "Aviso: esta operação irá sobrescrever a base de dados atual."
read -p "Deseja continuar? (s/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Operação cancelada."
    exit 0
fi

echo "Restaurando backup de ${ARQUIVO}..."

gunzip -c "${ARQUIVO}" | docker compose exec -T db psql -U "${DB_USER:-xpto}" -d "${DB_NAME:-xpto}"

echo "Restauração concluída com sucesso!"
