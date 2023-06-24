#!/usr/bin/env python3

from lib.analyzer import CertificateAnalyzer
from lib.args import process_args
from lib.output import TextResultFormatter, JsonResultFormatter, HtmlResultFormatter
from lib.util import fatal_error

import yaml
import os

CONFIG_FILE = "config.yml"

def load_config() -> dict:
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
      try:
        config = yaml.safe_load(f)
        return config
      except yaml.YAMLError as err:
        print(f"Warning: Invalid config file - {err}")
        return {}
  else:
    return {}


def main():
  args = process_args()

  config = load_config()

  analyzer = CertificateAnalyzer(args.pcap, config)
  result = analyzer.analyze()

  if args.output == "text":
    formatter = TextResultFormatter()
  elif args.output == "json":
    formatter = JsonResultFormatter()
  elif args.output == "html":
    formatter = HtmlResultFormatter()
  else:
    fatal_error(f"Invalid output option: {args.outpu}")
    
  formatter.generate_output(result)

  print(formatter.result())

if __name__ == "__main__":  
  main()
