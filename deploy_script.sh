#!/bin/bash
# Example deployment script
cd ~/LED
git pull origin develop  # Pull the latest changes from GitHub
pip install -r requirements.txt  # Install/update dependencies
sudo systemctl restart led-server.service  # Restart your service to apply changes
