import pyshark
import uuid

from .cert import CertificateChain
from .result import AnalysisResult, TlsRequestRecord
from .threat_intel import fetch_crowd_sec_ip_record, fetch_virus_total_record    
from .dns import get_ipv4_addresses_for_hostname


class TlsStreamAnalyzer:
  """
  The TlsStreamAnalyzer implements the logic of analyzing packets to extract
  certificates and assess if they are valid or not.  The class presently works
  on PCAP files using the PyShark / tshark library.
  """
  
  def __init__(self, pcap_file: str, config: dict[str, any], verbose: bool) -> None:
    """
    Creates a new TlsStreamAnalyzer.

    Parameters:
      pcap_file: The pcap file to analyze.
      config:    The tools configuration.
    """
    self.__pcap_file = pcap_file
    self.__result = None
    self.__verbose = verbose
    self.__config = config
    self.__client_hellos = {}
   
  def analyze(self) -> AnalysisResult:
    """
    The main method that will parse the specified pcap file,
    identify TLS connections, analyze certs and prepare return
    the result.

    Returns:
      The analysis results for the PCAP passed in, in the
      constructor.
    """
    
    if self.__verbose:
      print(f"Reading pcap: {self.__pcap_file}\n")
    
    self.__result = AnalysisResult(self.__pcap_file, [])
    
    data = pyshark.FileCapture(self.__pcap_file)

    for pkt in data:
      if "TLS" in pkt:
        self.__process_tls_packet(pkt, pkt["TLS"])

    if self.__verbose:
      print(f"\nFinished processing pcap file.")
    
    return self.__result

  ##
  ## Private Methods
  ##


  def __process_tls_packet(self, pkt, tls_layer) -> None:
    """
    A helper method that process a TLS packet, looking for the TLS
    handshake, which is record type 22.
    """
    if hasattr(tls_layer, "record_content_type") and tls_layer.record_content_type == "22":
       self.__process_tls_handshake_packet(pkt, tls_layer)


  def __process_tls_handshake_packet(self, pkt, tls_layer) -> None:
    """
    A helper method which processes the TLS handshake method, looking
    for either a Client Hello, a Server Hello, or a Certificate record.

    We must looks for the client hello, since that is where the Server
    Name Identification information is provided that communicates the
    requested hostname. See:
      https://datatracker.ietf.org/doc/html/rfc6066#section-3
    """
    # Client Hello
    if tls_layer.handshake_type == "1":
      self.__process_tls_handshake_client_hello_packet(pkt, tls_layer)

    # Server Hello
    elif tls_layer.handshake_type == "2" or  tls_layer.handshake_type == "11":
      self.__process_tls_handshake_certificate_packet(pkt, tls_layer)

  def __process_tls_handshake_client_hello_packet(self, pkt, tls_layer):
    """
    Processes the TLS Handshake Client Hello, and creates a record that
    maps the connection to the requested server name, so that we can
    use that information later when processing the cert.
    """
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
    """
    Processes a TLS packet that contains a certificate sent from the
    server to the client and evaluates the certificate.
    """
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
      server_hostname = server_ip

    if self.__verbose:
      print(f"Processing certificate for: {client_hello_key} ({server_hostname})")
    
    entity_cert_bytes = bytes.fromhex(certs_attr.raw_value)

    intermediates_certs = []
    for intermediate_bytes in certs_attr.alternate_fields:
      value = intermediate_bytes.raw_value
      intermediates_certs.append(bytes.fromhex(value))

    cert_chain = CertificateChain(entity_cert_bytes, intermediates_certs)
    
    valid_ip_for_domain = get_ipv4_addresses_for_hostname(server_hostname)    

    error = cert_chain.validate(server_hostname)

    crowd_sec_api_key = self.__config.get("crowd_sec_api_key", None)
    if crowd_sec_api_key != None:
      if self.__verbose:
        print(f"  Fetching CrowdSec results for '{server_ip}'...", end="")
      crowd_sec_record = fetch_crowd_sec_ip_record(server_ip, crowd_sec_api_key)
      if self.__verbose:
        print("Done.")
    else:
      crowd_sec_record = None

    virus_total_api_key = self.__config.get("virus_total_api_key", None)
    if virus_total_api_key != None:
      if self.__verbose:
        print(f"  Fetching Virus Total results for '{server_hostname}'...", end="")
      virus_total_record = fetch_virus_total_record(server_hostname, virus_total_api_key)
      if self.__verbose:
        print("Done.")
    else:
      virus_total_record = None

    record = TlsRequestRecord(
      uuid.uuid4(),
      server_ip, 
      valid_ip_for_domain,
      server_hostname,
      cert_chain,
      error,
      crowd_sec_record,
      virus_total_record
    )

    self.__result.tls_requests.append(record)

    if self.__verbose:
        print("")
