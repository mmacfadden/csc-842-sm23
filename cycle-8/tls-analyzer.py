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

  if config == None:
    config = {}

  analyzer = CertificateAnalyzer(args.pcap, config)
  result = analyzer.analyze()

  if args.format == "text":
    formatter = TextResultFormatter()
  elif args.format == "json":
    formatter = JsonResultFormatter()
  elif args.format == "html":
    formatter = HtmlResultFormatter()
  else:
    fatal_error(f"Invalid output option: {args.format}")
    
  formatter.generate_output(result)

  if args.output != None:
    with open(args.output, "w") as f:
      f.write(formatter.result())
  else:
    print(formatter.result())

if __name__ == "__main__":  
  main()
