import argparse

def process_args():
  """
  This method sets up the command line parser using argparse.
  """

  parser = argparse.ArgumentParser(
                      prog='tls-analyzer',
                      description='TBD.'
                      )

  parser.add_argument('-p', 
                      '--pcap',
                      dest="pcap",
                      required=True, 
                      help="The pcap file to read from")

  parser.add_argument('-c', 
                      '--config', 
                      required=False, 
                      dest="config", 
                      default=None,
                      help="Overrides the default config file name")  

  parser.add_argument('-f', 
                      '--format', 
                      required=False,
                      default="text",
                      choices=["text", "json", "html"],
                      help="Specifies the output format"
                      )
  
  parser.add_argument('-o', 
                      '--output', 
                      required=False,
                      default=None,
                      help="Saves output to a file instead of standard out"
                      )
  
  parser.add_argument('-v', 
                      '--verbose', 
                      required=False,
                      action="store_true",
                      default=False,
                      help="Triggers additional output while processing the pcap"
                      )

  args = parser.parse_args()

  return args