import socket

def get_ipv4_addresses_for_hostname(hostname: str) -> list[str]:
  ips = set()
  entries = socket.getaddrinfo(hostname, 0)
  for e in entries:
    if e[0] is socket.AddressFamily.AF_INET:
      ip = e[4][0]
      ips.add(ip)
  
  return list(ips)
