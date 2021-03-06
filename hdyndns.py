#!/usr/bin/env python3
from argparse import ArgumentParser
import requests

hetzner_base_url = "https://dns.hetzner.com/api/v1"
ip_info_url = "https://ipinfo.io/ip"

def get_public_ip() -> str:
    r = requests.get(ip_info_url)
    if r.status_code <= 399:
        return r.text

def configure_dns(clients, hetzner_zone_id, hetzner_token, delete=False):

    headers = {'Auth-API-Token': hetzner_token}
    records_url = hetzner_base_url + f'/records?zone_id={hetzner_zone_id}'
    record_id_url = hetzner_base_url + '/records/{record_id}'
    record_post_url = hetzner_base_url + '/records'

    r = requests.get(records_url, headers=headers)
    if r.status_code <= 399:
        existing_records = { e['name']: {'value': e['value'], 'id': e['id']} for e in r.json()['records'] if e['type'] == 'A' }
        client_names = list()

        for client in clients:
            client_name = f"{client['name']}"
            client_names.append(client_name)
            client_ip = client['ip']

            payload = {
                "zone_id": hetzner_zone_id,
                "type": "A",
                "name": client_name,
                "value": client_ip,
                "ttl": 60
            }

            if client_name in existing_records:
                if client_ip != existing_records[client_name]['value']:
                    print(f'updating ip for {client_name}')
                    r = requests.put(record_id_url.format(record_id=existing_records[client_name]['id']), headers=headers, json=payload)
                else:
                    print(f'{client_name} already has {client_ip}')
            else:
                print(f'posting new ip {client_ip} for {client_name}')
                r = requests.post(url=record_post_url, headers=headers, json=payload)
    else:
        return

def main():
    parser = ArgumentParser()
    parser.add_argument('--names', required=True, help="subdomain to update", nargs="+")
    parser.add_argument('--hetzner-token', '--ht', dest='hetzner_token', required=True, help="Hetzner api token")
    parser.add_argument('--hetzner-zone-id', '--hzi', dest='hetzner_zone_id', required=True, help="Hetzner zone id")
    args = parser.parse_args()


    client_ip = get_public_ip()
    if client_ip:
        clients = list()
        for name in args.names:
            clients.append({
                "name": name,
                "ip": client_ip
            })
        configure_dns(clients, args.hetzner_zone_id, args.hetzner_token)

if __name__ == '__main__':
    main()