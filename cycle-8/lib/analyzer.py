import pyshark


from .dns import validate_ip_address_for_domain
from .cert import CertificateChain

def process_tls_handshake_certificate_packet(pkt, tls_layer):
  ip = pkt['IP']
  source_ip = ip.src
  
  certs_attr = tls_layer.get_field("handshake_certificate")
  entity_cert_bytes = bytes.fromhex(certs_attr.raw_value)
  

  intermediates_certs = []
  for intermediate_bytes in certs_attr.alternate_fields:
    value = intermediate_bytes.raw_value
    intermediates_certs.append(bytes.fromhex(value))


  cert_chain = CertificateChain(entity_cert_bytes, intermediates_certs)
  
  hostname = cert_chain.hostname()

  print(f"{source_ip} -> {hostname}")

  valid_ip_for_domain = validate_ip_address_for_domain(source_ip, hostname)
  if valid_ip_for_domain:
    print("Valid IP for Domain")
  else:
    print("Invalid IP for Domain")

  cert_chain.validate()


  
    
 
def process_tls_handshake_packet(pkt, tls_layer) -> None:
   if tls_layer.handshake_type == "11":
      process_tls_handshake_certificate_packet(pkt, tls_layer)

def process_tls_packet(pkt, tls_layer) -> None:
  if hasattr(tls_layer, "record_content_type") and tls_layer.record_content_type == "22":
     process_tls_handshake_packet(pkt, tls_layer)

def analyze_pcap(pcap: str) -> None:
  data = pyshark.FileCapture(pcap)

  for pkt in data:
      if "TLS" in pkt:
        process_tls_packet(pkt, pkt["TLS"])