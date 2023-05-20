

import datetime


# def get_dates():
#    today = datetime.date.today()
#    this_week = today - datetime.timedelta(days=today.weekday() + 1)
#    last_week = this_week - datetime.timedelta(days=7)
#    return [last_week, this_week]
 

def get_dates():
  today = datetime.date.today()
  this_month = today.replace(day=1)
  last_month = this_month - datetime.timedelta(days=1)
  last_month = last_month.replace(day=1)
  return [last_month, this_month]

print(get_dates())

import urllib.request, json
# def get_seed(date):
#   stock_symbol = "AAPL"
  
#   url = f"https://api.marketdata.app/v1/stocks/candles/D/{stock_symbol}/?countback=1&to={str(date)}&dateformat=timestamp"
#   response = urllib.request.urlopen(url)
#   data = json.loads(response.read())
#   return data["c"][0]


def get_seed(date):
  lat = 52.52
  lng = 13.41
  metric = "temperature_2m_max"
  url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date={str(date)}&end_date={str(date)}&daily={metric}&timezone=America%2FLos_Angeles"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  return data["daily"][metric][0]

print(get_seed(datetime.date.today()))


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


print(generate_domain(0, 4))