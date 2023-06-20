import socket

def get_ipv4_by_hostname(hostname) -> list[str]:
  ips = set()
  entries = socket.getaddrinfo(hostname, 0)
  for e in entries:
    if e[0] is socket.AddressFamily.AF_INET:
      ip = e[4][0]
      ips.add(ip)
  
  return list(ips)


def validate_ip_address_for_domain(ip_address: str, hostname: str) -> bool:
    valid_ips = get_ipv4_by_hostname(hostname)
    valid = ip_address in valid_ips
    return valid