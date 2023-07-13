from mysql.connector import connect, Error

from colorama import Fore, Style

from ..secret_detector import SecretDetector
from ..db_scanner import DatabaseScanner, TableDetections
from ..util import fatal_error


class MySqlDbScanner(DatabaseScanner):

  def __init__(self, 
               detectors: list[SecretDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def scan(self) -> list[TableDetections]:
    detections = []

    if ":" in self.url:
      (host, port) = self.url.split(":")
    else:
      host = self.url
      port = 3306
    
    try:
      self._log(f"{Fore.YELLOW}Connecting to MySQL{Style.RESET_ALL}: {host}:{port}")
      with connect(
        host=host,
        port=port,
        user=self.username,
        password=self.password,
        database=self.db_name
      ) as connection:
        self._log(f"{Fore.GREEN}Successfully Connected.{Style.RESET_ALL}")

        table_names = self.get_table_names(connection)
        for table in table_names:
          table_detections = self.scan_table(connection, table)
          if table_detections != None:
            detections.append(table_detections)
    
    except Error as e:
      fatal_error(f"Could not connect to MySQL: {e}")
        
    return detections


  def get_table_names(self, connection) -> list[str]:
    table_names = []
    with connection.cursor() as cursor:
      cursor.execute("SHOW TABLES")
      for table in cursor:
        table_name = table[0]
        table_names.append(table_name)

    return table_names

  def scan_table(self, connection , table) -> TableDetections:
    detections = {}
    
    select_query = f"SELECT * FROM {table} LIMIT 5"
    with connection.cursor() as cursor:
      cursor.execute(select_query)
      for row in cursor:
        for value in row:
          if isinstance(value, str):
            new_detections = self.detect_secret(value)
            for nd in new_detections:
              if not nd.name in detections:
                detections[nd.name] = nd
            
      
    return TableDetections(table, detections.values())
  

def create_scanner(detectors: list[SecretDetector],
                  sample_size: int,
                  url: str, 
                  db_name: str, 
                  username: str, 
                  password: str,
                  verbose: bool) -> MySqlDbScanner:
  
  return MySqlDbScanner(detectors, sample_size, url, db_name, username, password, verbose)
