#!/bin/bash

# Check for root privileges 
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

# Copy essential files
cp -p -r ./src/ /etc/service-status-indicator-api/
# Create an empty services file
echo "[]" > /etc/service-status-indicator-api/services.json

# Ask for running port
read -p "Enter a PORT for the API [default: 8000]: " port
if [[ -z "$port" ]]; then
  port="8000"
fi
# Replace the port on server's staring script
sed -i "s/0\.0\.0\.0:{PORT}/0.0.0.0:$port/g" /etc/service-status-indicator-api/start-server.sh


# Ask for default interval
read -p "Enter a default check interval in seconds [default: 60]: " interval
if [[ -z "$interval" ]]; then
  interval="60"
fi
echo $interval > /etc/service-status-indicator-api/.service_status_indicator_default_update_interval


# Generate a key
key=$(openssl rand -base64 50 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c50)
echo $key > /etc/service-status-indicator-api/.service_status_indicator_api_token


# Enable systemd service
ln -s /etc/service-status-indicator-api/service-status-indicator-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now service-status-indicator-api.service


# Print the Token
echo "This will be your TOKEN: "
echo $key