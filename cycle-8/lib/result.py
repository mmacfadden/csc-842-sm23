from dataclasses import dataclass
from typing import Union

from .cert import CertificateChain, CertValidationError

@dataclass
class TlsRequestRecord:
  """
  The TlsRequestRecord represents a parsed and analyzed TLS Exchange that
  was found in the PCAP file.
  """
  uuid: str
  request_ip: str
  valid_ips_for_hostname: list[str]
  hostname: str
  cert_chain: CertificateChain
  cert_error: Union[CertValidationError, None]
  crowd_sec_record: dict
  virus_total_record: dict

  def has_errors(self) -> bool:
    # TODO Virus Total Response "data": { "attributes": { "threat_names": [],
    return self.cert_error != None

  @property
  def valid_ip_for_hostname(self) -> bool:
    return self.request_ip in self.valid_ips_for_hostname
  
  def to_data(self) -> dict[str, any]:
    """
    Serializes this record as a dict in support of JSON
    serialization.
    """

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
      "crowd_sec_record": self.crowd_sec_record,
      "virus_total_record": self.virus_total_record
    }


@dataclass
class AnalysisResult:
  """
  The AnalysisResult represents the total analysis results of a 
  specific PCAP file.
  """
  pcap_file: str
  tls_requests: list[TlsRequestRecord]

  def to_data(self) -> dict[str, any]:
    """
    Serializes this result object as a dict in support of JSON
    serialization.
    """
    return {
      "pcap_file": self.pcap_file,
      "tls_requests": list(map(lambda x: x.to_data(), self.tls_requests))
    }