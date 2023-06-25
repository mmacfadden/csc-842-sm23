import socket

def get_ipv4_addresses_for_hostname(hostname: str) -> list[str]:
  """
  A helper utility to see which IPV4 IP addresses are associated
  with this hostname.

  Parameters:
    The hostname to resolve IP addresses for.
  Returns:
    A list of valid IP addresses for the supplied hostname.
  """
  
  ips = set()
  try:
    entries = socket.getaddrinfo(hostname, 0)
    for e in entries:
      if e[0] is socket.AddressFamily.AF_INET:
        ip = e[4][0]
        ips.add(ip)
  except:
    pass
  
  return list(ips)
