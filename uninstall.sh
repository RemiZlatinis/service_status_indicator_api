#!/bin/bash

# Check for root privileges 
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi


# Disable systemd service
systemctl disable --now service-status-indicator-api.service


# Remove files
rm -rf /etc/service-status-indicator-api/