import argparse

def process_args():
  """
  This method sets up the command line parser using argparse.
  """

  parser = argparse.ArgumentParser(
                      prog='db-scavenger',
                      description='A tool that searches a database for sensitive data and supports extracting data of interest.'
                      )

  parser.add_argument('-t', 
                      '--type', 
                      required=True, 
                      dest="type", 
                      default=None,
                      help="Specifies the type of database you are connecting to") 
  
  parser.add_argument('-n', 
                      '--sample-size', 
                      required=False, 
                      dest="sample_size", 
                      default=10,
                      help="Specifies the number of records from each table to query to detect data") 

  parser.add_argument('-s', 
                      '--server', 
                      required=True, 
                      dest="server", 
                      default=None,
                      help="Specifies the database server to connect to")  

  parser.add_argument('-d', 
                      '--database', 
                      required=True, 
                      dest="database", 
                      default=None,
                      help="Specifies the database name to connect to")  

  parser.add_argument('-u', 
                      '--username', 
                      required=True, 
                      dest="username", 
                      default=None,
                      help="The username to log into the database with")  
  
  parser.add_argument('-p', 
                      '--password', 
                      required=True, 
                      dest="password", 
                      default=None,
                      help="The password to log into the database with")  
  
  parser.add_argument('-e', 
                      '--extract', 
                      required=False,
                      default=None,
                      type=str,
                      help="Extracts detected data from the database to a specified file"
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