#!/usr/bin/env python3

import yaml
import os
from typing import Union

from lib.args import process_args
from lib.util import fatal_error

from lib.analyzer import TlsStreamAnalyzer
from lib.result import AnalysisResult
from lib.output import TextResultFormatter, JsonResultFormatter, HtmlResultFormatter


DEFAULT_CONFIG_FILE = "config.yml"


def load_config(config_file: Union[None, str]) -> dict[str, any]:
  """
  A helper method to load the config file from disk.
  """

  if config_file != None:
    file_name = config_file
  else:
    file_name = DEFAULT_CONFIG_FILE
  
  if os.path.exists(file_name):
    with open(file_name, "r") as f:
      try:
        config = yaml.safe_load(f)

        # This occurs if the YAML file is empty or contains
        # no root keys.
        if config == None:
          config = {}

        return config
      except yaml.YAMLError as err:
        fatal_error(f"Invalid config file: {err}")
  elif config_file != None:
    # The user specified a config file, but we can't read it.
    fatal_error(f"The specified config file could not be read: {config_file}")
  else:
    # The user did not specify a config file, and the default one
    # doesn't exist, so just return an empty config.
    return {}


def output_results(result: AnalysisResult, format: str, output: Union[str, None]) -> None:
  """
  A helper method to output the analysis results.

  Parameters:
    format: The format to out put in. This must be on of "json", "text", 
            or "html".
    output: An optional filename to output the results to.  If not specified,
            then output will be made to standard out.
  """
  if format == "text":
    formatter = TextResultFormatter()
  elif format == "json":
    formatter = JsonResultFormatter()
  elif format == "html":
    formatter = HtmlResultFormatter()
  else:
    fatal_error(f"Invalid output option: {format}")
    
  formatter.generate_output(result)

  if output != None:
    with open(output, "w") as f:
      f.write(formatter.result())
  else:
    print(formatter.result())


def analyze_pcap():
  """
  The main method that will analyze the specified pcap file.
  """

  args = process_args()

  config = load_config(args.config)

  analyzer = TlsStreamAnalyzer(args.pcap, config, args.verbose)
  result = analyzer.analyze()

  output_results(result, args.format, args.output)


if __name__ == "__main__":  
  analyze_pcap()
