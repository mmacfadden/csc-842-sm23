import requests
import base64


def fetch_crowd_sec_ip_record(ip: str, api_key: str) -> dict[str, any]:
  """
  Submits an ip to the CrowdSec API to see if it is deemed suspicious.

  Parameters:
    ip:      The ip address of the server from the TLS Request.
    api_key: The CrowdSec API Key from the config file.

  Returns:
    The raw response from CrowdSec as a parsed JSON object.
  """
  headers = {"x-api-key": api_key}
  url = f"https://cti.api.crowdsec.net/v2/smoke/{ip}"
  response = requests.get(url, headers=headers)
  
  return response.json()


def fetch_virus_total_record(hostname: str, api_key: str) -> dict[str, any]:
  """
  Submits the hostname to the VirusTotal API to see if it is deemed malicious.

  Parameters:
    hostname:  The hostname from the TLS Request.
    api_key:   The Virus Total API Key from the config file.

  Returns:
    The raw response from Virus Total as a parsed JSON object.
  """
  headers = {"x-apikey": api_key}
  encoded_hostname = base64.b64encode(hostname.encode("utf8")).decode("utf8").replace("=", "")
  url = f"https://www.virustotal.com/api/v3/urls/{encoded_hostname}"
  response = requests.get(url, headers=headers)

  return response.json()