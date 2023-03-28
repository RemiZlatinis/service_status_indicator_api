#!/bin/bash

if ! command -v flask &> /dev/null; then
    echo "Flask is not installed."
    exit 1
fi

if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn is not installed."
    exit 1
fi

cd /etc/service-status-indicator-api/
export SERVICE_STATUS_INDICATOR_API_TOKEN=$(cat .service_status_indicator_api_token) 
export SERVICE_STATUS_INDICATOR_DEFAULT_UPDATE_INTERVAL=$(cat .service_status_indicator_default_update_interval) 
gunicorn -b 0.0.0.0:{PORT} wsgi:app --log-level=info --log-file=/var/log/gunicorn.log
