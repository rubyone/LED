#!/usr/bin/env bash
# Collect a quick diagnostic snapshot for the LED server environment.
OUTDIR="/tmp/led_debug_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTDIR"
LOG(){ echo "[debug] $*"; }
LOG "Writing snapshot to $OUTDIR"

# Service status
systemctl status led-server >"$OUTDIR/service_status.txt" 2>&1 || true

# Recent journal
journalctl -u led-server -n 200 >"$OUTDIR/journal_tail.txt" 2>&1 || true

# Log files
cp /var/log/led-server.log "$OUTDIR/" 2>/dev/null || true
cp /var/log/led-server.error.log "$OUTDIR/" 2>/dev/null || true

# Open ports
ss -tulpn >"$OUTDIR/listening_sockets.txt" 2>&1 || true

# Processes
ps -ef | grep -i led_server | grep -v grep >"$OUTDIR/processes.txt" 2>&1 || true

# Config snapshot
if [[ -f /home/pi/LED/config.json ]]; then
  cp /home/pi/LED/config.json "$OUTDIR/" 2>/dev/null || true
fi

# Python environment
python3 -V >"$OUTDIR/python_env.txt" 2>&1 || true
which python3 >>"$OUTDIR/python_env.txt" 2>&1 || true
pip3 freeze >"$OUTDIR/pip_freeze.txt" 2>&1 || true

# Disk + memory
free -h >"$OUTDIR/memory.txt" 2>&1 || true
df -h >"$OUTDIR/disk.txt" 2>&1 || true

# Network
ip addr show >"$OUTDIR/ip_addr.txt" 2>&1 || true
ip route show >"$OUTDIR/ip_route.txt" 2>&1 || true

LOG "Snapshot created: $OUTDIR"
LOG "Create tarball with: tar czf ${OUTDIR}.tar.gz -C /tmp $(basename $OUTDIR)"
