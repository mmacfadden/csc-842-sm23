import pyshark
import uuid
from dataclasses import dataclass
from typing import Union

from .dns import get_ipv4_addresses_for_hostname
from .cert import CertificateChain, CertValidationError
from .threat_intel import fetch_crowd_sec_ip_record, fetch_virus_total_record

@dataclass
class TlsRequestRecord:
  uuid: str
  request_ip: str
  valid_ips_for_hostname: list[str]
  hostname: str
  cert_chain: CertificateChain
  cert_error: Union[CertValidationError, None]
  crowd_sec_ip_record: dict
  virus_total_ip_record: dict

  def has_errors(self) -> bool:
    # TODO Virust Total Response "data": { "attributes": { "threat_names": [],
    return self.cert_error != None

  @property
  def valid_ip_for_hostname(self) -> bool:
    return self.request_ip in self.valid_ips_for_hostname
  
  def to_data(self) -> dict:
    cert_error = None
    if self.cert_error != None:
      cert_error = self.cert_error.to_data()

    return {
      "request_ip": self.request_ip,
      "valid_ip_for_hostname": self.valid_ip_for_hostname,
      "valid_ips_for_hostname": self.valid_ips_for_hostname,
      "hostname": self.hostname,
      "cert_chain": self.cert_chain.to_data(),
      "cert_error": cert_error,
      "crowd_sec_ip_record": self.crowd_sec_ip_record,
      "virus_total_ip_record": self.virus_total_ip_record
    }

@dataclass
class AnalysisResult:
  pcap_file: str
  tls_requests: list[TlsRequestRecord]

  def to_data(self) -> dict[str, any]:
    return {
      "pcap_file": self.pcap_file,
      "tls_requests": list(map(lambda x: x.to_data(), self.tls_requests))
    }
    
  
class CertificateAnalyzer:
  def __init__(self, pcap_file: str, config: dict) -> None:
    self.__pcap_file = pcap_file
    self.__result = None
    self.__config = config
    self.__client_hellos = {}
   
  def analyze(self) -> AnalysisResult:
    self.__result = AnalysisResult(self.__pcap_file, [])
    
    data = pyshark.FileCapture(self.__pcap_file)

    for pkt in data:
      if "TLS" in pkt:
        self.__process_tls_packet(pkt, pkt["TLS"])
    
    return self.__result

  def __process_tls_packet(self, pkt, tls_layer) -> None:
    if hasattr(tls_layer, "record_content_type") and tls_layer.record_content_type == "22":
       self.__process_tls_handshake_packet(pkt, tls_layer)

  def __process_tls_handshake_packet(self, pkt, tls_layer) -> None:
    # Client Hello
    if tls_layer.handshake_type == "1":
      self.__process_tls_handshake_client_hello_packet(pkt, tls_layer)

    # Server Hello
    elif tls_layer.handshake_type == "2" or  tls_layer.handshake_type == "11":
      self.__process_tls_handshake_certificate_packet(pkt, tls_layer)

  def __process_tls_handshake_client_hello_packet(self, pkt, tls_layer):
    server_name = tls_layer.get_field("handshake_extensions_server_name")
    if server_name != None:
      client_ip = str(pkt['IP'].src)
      client_port = str(pkt['TCP'].srcport)
      server_ip = str(pkt['IP'].dst)
      server_port = str(pkt['TCP'].dstport)
      key = f"{client_ip}:{client_port}->{server_ip}:{server_port}"
      self.__client_hellos[key] = {
        "server_hostname": server_name
      }

  def __process_tls_handshake_certificate_packet(self, pkt, tls_layer):
    certs_attr = tls_layer.get_field("handshake_certificate")
    if certs_attr == None:
      return
    
    client_ip = str(pkt['IP'].dst)
    client_port = str(pkt['TCP'].dstport)
    server_ip = str(pkt['IP'].src)
    server_port = str(pkt['TCP'].srcport)
    client_hello_key = f"{client_ip}:{client_port}->{server_ip}:{server_port}"

    client_hello = self.__client_hellos.get(client_hello_key)
    if client_hello != None:
      server_hostname = client_hello.get("server_hostname")
    else:
      # Try to get it from the cert itself.
      server_hostname = cert_chain.hostname()
    
    entity_cert_bytes = bytes.fromhex(certs_attr.raw_value)

    intermediates_certs = []
    for intermediate_bytes in certs_attr.alternate_fields:
      value = intermediate_bytes.raw_value
      intermediates_certs.append(bytes.fromhex(value))

    cert_chain = CertificateChain(entity_cert_bytes, intermediates_certs)
    
    valid_ip_for_domain = get_ipv4_addresses_for_hostname(server_hostname)    

    error = cert_chain.validate(server_hostname)

    # cert_chain.validate_cert()

    crowd_sec_api_key = self.__config.get("crowd_sec_api_key", None)
    if crowd_sec_api_key != None:
      crowd_sec_ip_record = fetch_crowd_sec_ip_record(server_ip, crowd_sec_api_key)
    else:
      crowd_sec_ip_record = None

    virus_total_api_key = self.__config.get("virus_total_api_key", None)
    if virus_total_api_key != None:
      virus_total_ip_record = fetch_virus_total_record(server_ip, virus_total_api_key)
    else:
      virus_total_ip_record = None

    record = TlsRequestRecord(
      uuid.uuid4(),
      server_ip, 
      valid_ip_for_domain,
      server_hostname,
      cert_chain,
      error,
      crowd_sec_ip_record,
      virus_total_ip_record
    )

    self.__result.tls_requests.append(record)
      
  