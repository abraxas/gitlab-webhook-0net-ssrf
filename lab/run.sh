#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-gitlab-webhook-0net-ssrf}"
export GITLAB_URL="${GITLAB_URL:-http://127.0.0.1:18420}"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 25); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 60
  down
done
if [[ "${up_ok}" != 1 ]]; then
  echo "FAIL GITLAB-WEBHOOK-0NET-SSRF compose up failed" | tee poc-last-run.txt
  down
  exit 1
fi

echo "== wait GitLab sign_in =="
ready=0
for i in $(seq 1 150); do
  code=$(curl -sS -o /tmp/gitlab-webhook-0net-sign_in.html -w '%{http_code}' --max-time 8 \
    -H 'Accept: text/html' "${GITLAB_URL}/users/sign_in" || true)
  if [[ "${code}" == "200" ]] && grep -qi 'sign in' /tmp/gitlab-webhook-0net-sign_in.html 2>/dev/null; then
    ready=1
    echo "gitlab-ready attempt=${i} http=${code}"
    break
  fi
  echo "gitlab-wait attempt=${i} http=${code}"
  sleep 8
done
if [[ "${ready}" != 1 ]]; then
  echo "FAIL GITLAB-WEBHOOK-0NET-SSRF gitlab not ready" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --tail=80 || true
  down
  exit 1
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e
if [[ "${rc}" != 0 ]]; then
  if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
    echo "FAIL GITLAB-WEBHOOK-0NET-SSRF poc exit=${rc}" >> poc-last-run.txt
  fi
fi

down
exit "${rc}"
