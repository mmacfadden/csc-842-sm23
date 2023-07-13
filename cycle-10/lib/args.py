import argparse

def process_args():
  """
  This method sets up the command line parser using argparse.
  """

  parser = argparse.ArgumentParser(
                      prog='db-secret-finder',
                      description='TBD'
                      )


  parser.add_argument('-t', 
                      '--type', 
                      required=True, 
                      dest="type", 
                      default=None,
                      help="Specifies the configuration file") 
  
  parser.add_argument('-n', 
                      '--sample-size', 
                      required=False, 
                      dest="sample_size", 
                      default=5,
                      help="Specifies the configuration file") 

  parser.add_argument('-s', 
                      '--server', 
                      required=True, 
                      dest="server", 
                      default=None,
                      help="Specifies the configuration file")  

  parser.add_argument('-d', 
                      '--database', 
                      required=True, 
                      dest="database", 
                      default=None,
                      help="Specifies the configuration file")  

  parser.add_argument('-u', 
                      '--username', 
                      required=True, 
                      dest="username", 
                      default=None,
                      help="Specifies the configuration file")  
  
  parser.add_argument('-p', 
                      '--password', 
                      required=True, 
                      dest="password", 
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