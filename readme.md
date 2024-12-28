# LED Strip Web Controller

A web-based controller for WS281x LED strips using Raspberry Pi.
Control your LED animations through an easy-to-use python flask web interface.

```sh
# Remove all ._ files before committing
find . -name "._*" -delete         
```

## Features

- 🌈 Multiple animation patterns
- 🎨 Static color controls
- 🔆 Brightness adjustment
- 🌐 Web-based interface
- 🔄 Auto-restart capability
- 📝 Detailed logging
- 🚀 Runs as a system service

## Usage

1. Access the web interface:

## Hardware Setup

- Compatible with WS281x LED strips
- Default configuration:
   - LED Count: 41
   - GPIO Pin: 18
   - LED Frequency: 800000 Hz
   - DMA Channel: 10
   - Brightness: 255
   - Channel: 0

## Configuration

Edit `LED1.py` to modify LED strip parameters:

3. Common issues:

- Permission denied: Make sure you're running as the 'pi' user
- Port already in use: Check if another instance is running
- LED strip not responding: Verify GPIO connections

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the rpi_ws281x library
- Web interface built with Flask
- Systemd service management

```sh
# Copy the service file to systemd directory
sudo cp led-server.service /etc/systemd/system/

# Create log files and set permissions
sudo touch /var/log/led-server.log
sudo touch /var/log/led-server.error.log

# Make sure log files have correct permissions
sudo chown root:root /var/log/led-server.log /var/log/led-server.error.log

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable led-server

# Start the service
sudo systemctl start led-server

# Stop the service
sudo systemctl stop led-server

# Disable service from starting on boot
sudo systemctl disable led-server

# Check service status
sudo systemctl status led-server

# Restart the service
sudo systemctl restart led-server

# For viewing logs 

# View real-time logs
sudo journalctl -u led-server -f

# View service logs
tail -f /var/log/led-server.log

# View error logs
tail -f /var/log/led-server.error.log


```

```sh
sudo cp led-server.logrotate /etc/logrotate.d/led-server
```