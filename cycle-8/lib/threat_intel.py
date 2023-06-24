import requests
import json
import base64


def fetch_crowd_sec_ip_record(ip: str, api_key: str) -> str:
    headers = {"x-api-key": api_key}
    url = f"https://cti.api.crowdsec.net/v2/smoke/{ip}"
 
    response = requests.get(url, headers=headers)

    return response.json()


def fetch_virus_total_record(ip: str, api_key: str) -> str:
    headers = {"x-apikey": api_key}
    encoded_ip = base64.b64encode(ip.encode("utf8")).decode("utf8").replace("=", "")
    url = f"https://www.virustotal.com/api/v3/urls/{encoded_ip}"
    response = requests.get(url, headers=headers)

    return response.json()