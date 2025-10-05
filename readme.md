# LED Strip Web Controller

A web-based controller for WS281x LED strips using Raspberry Pi.
Control your LED animations through an easy-to-use python flask web interface.

```sh
# Remove all ._ files before committing
find . -name "._*" -delete         
# LED Strip Web Controller

Web-based control panel for WS281x (NeoPixel) LED strips running on a Raspberry Pi. Provides static colors, animations, brightness control and a simple REST API.

---
## ✨ Features
* 🌈 Multiple animations (rainbow, fire effect, theater chase, etc.)
* 🎨 Static colors + custom RGB picker (web UI)
* 🔆 Brightness slider
* 🚦 Live LED preview (browser)
* 🖥️ Runs as systemd service (auto-start on boot)
* ♻️ Hot-reload support via watcher script OR API endpoint
* � Debug helper script for quick diagnostics
* 📝 Rotating log files under `/var/log/`

---
## 🧰 Hardware
| Item | Notes |
|------|-------|
| Raspberry Pi | Any model with PWM pin 18 recommended |
| LED Strip | WS2812/WS281x compatible |
| Power Supply | Size for LED count (≈60mA per full-white pixel) |
| Logic Level Shifter (recommended) | 3.3V Pi -> 5V data |

Defaults (overridden by `config.json`):
```
GPIO Pin: 18 (PWM)
LED Count: from config.json entry
Brightness: 255
Frequency: 800kHz
DMA: 10
Channel: 0
```

---
## 📁 Key Files
| File | Purpose |
|------|---------|
| `led_server.py` | Flask web server & API |
| `LED1.py` | LED controller + animations |
| `config.json` | Per-machine LED count & pin mapping |
| `led-server.service` | systemd unit definition |
| `reload_watcher.sh` | Auto-restart on file change |
| `debug_snapshot.sh` | Collect diagnostics snapshot |

---
## 🔧 Installation
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git
sudo pip3 install rpi_ws281x flask inquirer
sudo apt install -y inotify-tools  # optional for watcher

cd /home/pi/LED
sudo cp led-server.service /etc/systemd/system/led-server.service
sudo touch /var/log/led-server.log /var/log/led-server.error.log
sudo chown root:root /var/log/led-server.log /var/log/led-server.error.log
sudo systemctl daemon-reload
sudo systemctl enable led-server
sudo systemctl start led-server
```

Browse: `http://raspberrypi.local` (or the Pi's IP).

---
## ♻️ Reloading After Code Changes
Changes to `LED1.py`, `led_server.py`, or `config.json` need a reload.

### A. Manual Restart
```bash
sudo systemctl restart led-server
```

### B. API Reload (reinitializes controller)
```bash
curl -X POST http://raspberrypi.local/admin/reload
```
Use this when only LED count / pin / brightness defaults changed.

### C. Auto Watcher
```bash
chmod +x reload_watcher.sh
./reload_watcher.sh
```
Watches: `LED1.py`, `led_server.py`, `config.json`, `led-server.service`.

---
## 🧪 Testing LED Count Updates
1. Edit `config.json` (or logic in `LED1.py`).
2. Apply via API reload or full restart.
3. Verify log:
```bash
grep "Reload successful" /var/log/led-server.log
```

---
## 🧵 systemd Commands
```bash
sudo systemctl start led-server
sudo systemctl stop led-server
sudo systemctl restart led-server
sudo systemctl status led-server
sudo systemctl enable led-server
sudo systemctl disable led-server
sudo systemctl reload led-server   # sends HUP (ExecReload)
```

Update service after editing local file:
```bash
sudo cp /home/pi/LED/led-server.service /etc/systemd/system/led-server.service
sudo systemctl daemon-reload
sudo systemctl restart led-server
```

---
## 📊 Logs & Debugging
```bash
tail -f /var/log/led-server.log
tail -f /var/log/led-server.error.log
sudo journalctl -u led-server -f
chmod +x debug_snapshot.sh && ./debug_snapshot.sh
```

Common Issues:
| Symptom | Fix |
|---------|-----|
| No LEDs | Check power & ground continuity, correct GPIO (18) |
| Flicker / partial | Undersized PSU / voltage drop |
| PermissionError logs | Ensure service runs as root; log file perms |
| Blank page in Brave | Disable HTTPS upgrade / Shields for LAN IP |

---
## 🔐 Reload Endpoint
`POST /admin/reload` — Only allowed from local LAN (192.168.*) or localhost. Rebuilds controller instance.

---
## 🧹 Maintenance
```bash
sudo cp led-server.logrotate /etc/logrotate.d/led-server  # optional
find . -name '._*' -delete  # remove macOS metadata
```

---
## 🏗 Contributing
1. Fork → 2. Branch → 3. Commit → 4. PR

## 📄 License
MIT (see `LICENSE`).

## 🙏 Acknowledgments
* rpi_ws281x
* Flask
* Systemd

---
## 🔖 Quick Reference
```bash
sudo systemctl status led-server
sudo systemctl restart led-server
curl -X POST http://raspberrypi.local/admin/reload
tail -n 50 /var/log/led-server.log
./debug_snapshot.sh
```