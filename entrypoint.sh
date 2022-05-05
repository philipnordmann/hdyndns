#!/bin/sh

while true; do
    /opt/hdyndns/hdyndns.py \
        --delete \
        --name ${SUBDOMAIN_NAME} \
        --hetzner-token ${HETZNER_TOKEN} \
        --hetzner-zone-id ${HETZNER_ZONE_ID}
    sleep ${UPDATE_RATE:-60}
done