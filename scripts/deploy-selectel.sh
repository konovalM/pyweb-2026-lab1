#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Деплой статического сайта на отечественный хостинг (сервер Selectel) по SSH.
# Поднимает ИЗОЛИРОВАННЫЙ контейнер nginx на свободном порту 80 — не затрагивая
# остальные сервисы на сервере (ТГ-бот ai-system, 3x-ui, Portainer и т.д.).
#
# Запуск:  bash scripts/deploy-selectel.sh
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")/.."

# --- параметры сервера ---
HOST="94.154.130.35"
USER="root"
KEY="$HOME/.ssh/id_ed25519_uz"
REMOTE_DIR="/opt/ps-research"
SITE_URL="http://94.154.130.35.sslip.io/"
# IdentitiesOnly + отключённый agent — иначе ssh упирается в «too many auth failures»
SSH_OPTS=(-o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -i "$KEY")
remote() { env -u SSH_AUTH_SOCK ssh "${SSH_OPTS[@]}" "$USER@$HOST" "$@"; }

echo "==> 1/4 Строгая сборка сайта под адрес $SITE_URL"
source .venv/bin/activate
SITE_URL="$SITE_URL" mkdocs build --strict -d site-selectel

echo "==> 2/4 Заливка статики (rsync, с удалением лишнего)"
remote "mkdir -p $REMOTE_DIR/html"
env -u SSH_AUTH_SOCK rsync -az --delete \
  -e "ssh ${SSH_OPTS[*]}" \
  site-selectel/ "$USER@$HOST:$REMOTE_DIR/html/"

echo "==> 3/4 (Пере)запуск изолированного контейнера nginx на :80"
remote "cat > $REMOTE_DIR/nginx.conf" <<'CONF'
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;
    location / { try_files $uri $uri/ $uri/index.html =404; }
    error_page 404 /404.html;
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;
}
CONF
remote "docker rm -f ps-research 2>/dev/null || true; \
  docker run -d --name ps-research --restart unless-stopped \
    -p 80:80 \
    -v $REMOTE_DIR/html:/usr/share/nginx/html:ro \
    -v $REMOTE_DIR/nginx.conf:/etc/nginx/conf.d/default.conf:ro \
    nginx:alpine"

echo "==> 4/4 Healthcheck ($SITE_URL)"
code=$(curl -s -o /tmp/hc.html -w "%{http_code}" --max-time 15 "$SITE_URL")
echo "HTTP $code"
test "$code" = "200"
grep -q "PS-RESEARCH-LIVE" /tmp/hc.html \
  && echo "Контрольная строка найдена — деплой успешен" \
  || { echo "Контрольная строка НЕ найдена"; exit 1; }
