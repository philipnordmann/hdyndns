#!/bin/sh

while true; do
    /opt/hdyndns/hdyndns.py \
        --names ${SUBDOMAIN_NAMES} \
        --hetzner-token ${HETZNER_TOKEN} \
        --hetzner-zone-id ${HETZNER_ZONE_ID}
    sleep ${UPDATE_RATE:-60}
done