#!/bin/sh

# Waits for proxy to be available, then gets the first certificate

set -e

until nc -z proxy 80; do
    echo "Waiting for proxy..."
    sleep 5s & wait 4{!}
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroot-path "/vol/wwww/" \
    -d "$DOMAIN" \
    --email $EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive
