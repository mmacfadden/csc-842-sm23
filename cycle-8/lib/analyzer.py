import pyshark

from dataclasses import dataclass
from typing import Union


from .dns import get_ipv4_addresses_for_hostname
from .cert import CertificateChain

@dataclass
class CertificateRecord:
  request_ip: str
  valid_ips_for_hostname: list[str]
  hostname: str
  cert: CertificateChain
  error: Union[str, None]

  @property
  def valid_ip_for_hostname(self) -> bool:
    return self.request_ip in self.valid_ip_for_hostname

@dataclass
class AnalysisResult:
  pcap_file: str
  certificates: list[CertificateRecord]
  # def __init__(self, pcap_file: str) -> None:
  #   self.__pcap_file = pcap_file
  #   self.__certificates= []
  
  # @property
  # def pcap_file(self) -> str:
  #   return self.__pcap_file
  
  # @property
  # def certificates(self) -> str:
  #   return self.__certificates
  
  # def add_certificate(self, record: CertificateRecord) -> None:
  #   self.__certificates.append(record)

  # def __repr__(self) -> str:
    
  
class CertificateAnalyzer:
  def __init__(self, pcap_file: str) -> None:
    self.__pcap_file = pcap_file
    self.__result = None
   
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
    if tls_layer.handshake_type == "11" or tls_layer.handshake_type == "2":
      self.__process_tls_handshake_certificate_packet(pkt, tls_layer)

  def __process_tls_handshake_certificate_packet(self, pkt, tls_layer):
    ip = pkt['IP']
    source_ip = ip.src
    
    certs_attr = tls_layer.get_field("handshake_certificate")
    if certs_attr == None:
      return
    
    entity_cert_bytes = bytes.fromhex(certs_attr.raw_value)
    

    intermediates_certs = []
    for intermediate_bytes in certs_attr.alternate_fields:
      value = intermediate_bytes.raw_value
      intermediates_certs.append(bytes.fromhex(value))

    cert_chain = CertificateChain(entity_cert_bytes, intermediates_certs)
    
    hostname = cert_chain.hostname()

    valid_ip_for_domain = get_ipv4_addresses_for_hostname(hostname)    

    error = cert_chain.validate()

    record = CertificateRecord(source_ip, valid_ip_for_domain, hostname, cert_chain, error)

    self.__result.certificates.append(record)
      
  