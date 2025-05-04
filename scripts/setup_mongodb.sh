#!/bin/bash
# Install MongoDB (for Ubuntu/Debian-based systems)
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
# Create database directory
mkdir -p /data/db
# Verify MongoDB is running
mongo --version