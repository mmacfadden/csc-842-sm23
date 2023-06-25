import argparse
from .util import fatal_error

def process_args():
  """
  This method sets up the command line parser using argparse.  After argparse
  parses the command line args, this method then performs some additional
  sanity checking to make sure the arguments passed in are valid.
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

  parser.add_argument('-v', 
                      '--verbose', 
                      required=False, 
                      action='store_true', 
                      dest="verbose", 
                      default=False,
                      help="triggers verbose output")  

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

  args = parser.parse_args()

  return args