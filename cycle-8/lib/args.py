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

  parser.add_argument('-j', 
                      '--json', 
                      required=False, 
                      help="Output as JSON"
                      )

  args = parser.parse_args()

  return args