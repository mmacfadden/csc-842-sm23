
import datetime

def get_dates():
  today = datetime.date.today()
  this_month = today.replace(day=1)
  last_month = this_month - datetime.timedelta(days=1)
  last_month = last_month.replace(day=1)
  return [last_month, this_month]

import urllib.request, json, math
def get_seed(date):             
  url = f"https://api.marketdata.app/v1/stocks/candles/D/AAPL/?countback=1&to={str(date)}&dateformat=timestamp"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  return math.floor(data["c"][0] * 10)

valid_domain_chars = "1q3ag0n8fslwkti4u6952yzbvhdpocm7ej-rx"

def generate_domain(domain_index, seed):
  i = 0
  idx = (seed + domain_index) % len(valid_domain_chars)
  domain = ""

  while True:
    if i >= 10:
      break

    ch = valid_domain_chars[idx]
    domain += ch

    idx = ord(ch) + i
    idx = idx % len(valid_domain_chars)
    i = i + 1

  return domain

tlds = ['re', 'ru', 'xyz', 'za']

def generate_domains():
  domains = []
  domain_idx = 0

  dates = get_dates()

  for d in dates:
    seed = get_seed(d)
    for tld in tlds:
      for  i in range(0, 2):
        domain = generate_domain(domain_idx, seed)
        domain_idx = domain_idx + 1
        domains.append(domain + "." + tld)

  return domains


print(generate_domains())
