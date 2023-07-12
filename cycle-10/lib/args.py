import argparse

def process_args():
  """
  This method sets up the command line parser using argparse.
  """

  parser = argparse.ArgumentParser(
                      prog='db-secret-finder',
                      description='TBD'
                      )


  parser.add_argument('-c', 
                      '--config', 
                      required=False, 
                      dest="config", 
                      default=None,
                      help="Specifies the configuration file")  

  
  parser.add_argument('-e', 
                      '--extract', 
                      required=False,
                      default=None,
                      help="Saves output to a file instead of standard out"
                      )
  
  parser.add_argument('-v', 
                      '--verbose', 
                      required=False,
                      action="store_true",
                      default=False,
                      help="Triggers additional output"
                      )

  args = parser.parse_args()

  return args