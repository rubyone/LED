#!/usr/bin/env bash
# reload_watcher.sh - Auto-restart led-server systemd service when key files change.
# Requires: inotifywait (inotify-tools) or falls back to periodic checksum polling.

SERVICE_NAME="led-server"
WATCH_DIR="/home/pi/LED"
FILES_TO_WATCH=("LED1.py" "led_server.py" "config.json" "led-server.service")
INTERVAL=5
LOG_TAG="[reload-watcher]"

command -v inotifywait >/dev/null 2>&1 && HAVE_INOTIFY=1 || HAVE_INOTIFY=0

log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') ${LOG_TAG} $*"; }

restart_service(){
  if [[ -f "${WATCH_DIR}/led-server.service" ]]; then
    # If service file changed copy & reload daemon
    sudo cp "${WATCH_DIR}/led-server.service" /etc/systemd/system/led-server.service 2>/dev/null || true
    sudo systemctl daemon-reload || true
  fi
  log "Restarting ${SERVICE_NAME} due to file change: $1"
  sudo systemctl restart "${SERVICE_NAME}" && log "Restart successful" || log "Restart FAILED"
}

if [[ ${HAVE_INOTIFY} -eq 1 ]]; then
  log "Using inotify for change detection"
  while true; do
    inotifywait -e modify,close_write,move,create,delete "${WATCH_DIR}" \
      --format '%w%f' -q 2>/dev/null | while read changed; do
        for f in "${FILES_TO_WATCH[@]}"; do
          if [[ "${changed}" == "${WATCH_DIR}/${f}" ]]; then
            restart_service "${f}"
          fi
        done
      done
  done
else
  log "inotifywait not found - falling back to checksum polling (interval ${INTERVAL}s)"
  declare -A LAST_SUM
  for f in "${FILES_TO_WATCH[@]}"; do
    if [[ -f "${WATCH_DIR}/${f}" ]]; then
      LAST_SUM["$f"]=$(sha256sum "${WATCH_DIR}/${f}" | awk '{print $1}')
    else
      LAST_SUM["$f"]=missing
    fi
  done
  while true; do
    sleep ${INTERVAL}
    for f in "${FILES_TO_WATCH[@]}"; do
      path="${WATCH_DIR}/${f}"
      if [[ -f "${path}" ]]; then
        new_sum=$(sha256sum "${path}" | awk '{print $1}')
      else
        new_sum=missing
      fi
      if [[ "${new_sum}" != "${LAST_SUM[$f]}" ]]; then
        LAST_SUM["$f"]="${new_sum}"
        restart_service "${f}"
      fi
    done
  done
fi
