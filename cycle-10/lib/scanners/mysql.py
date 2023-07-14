from mysql.connector import connect, Error

from colorama import Fore, Style

from ..data_detector import DataDetector
from ..abstract_sql_scanner import AbstractSqlScanner
from ..util import fatal_error

class MySqlDbScanner(AbstractSqlScanner):

  def __init__(self, 
               detectors: list[DataDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def _create_connection(self) -> any:
    if ":" in self.url:
      (host, port) = self.url.split(":")
    else:
      host = self.url
      port = 3306
    
    try:
      self._log(f"{Fore.YELLOW}Connecting to MySQL{Style.RESET_ALL}: {host}:{port}")
      connection = connect(
        host=host,
        port=port,
        user=self.username,
        password=self.password,
        database=self.db_name
      )
      self._log(f"{Fore.GREEN}Successfully Connected.{Style.RESET_ALL}")

      return connection
    
    except Error as e:
      fatal_error(f"Could not connect to MySQL: {e}")

  def _get_table_names(self, connection) -> list[str]:
    table_names = []
    with connection.cursor() as cursor:
      cursor.execute("SHOW TABLES")
      for table in cursor:
        table_name = table[0]
        table_names.append(table_name)

    return table_names
  

def create_scanner(detectors: list[DataDetector],
                  sample_size: int,
                  url: str, 
                  db_name: str, 
                  username: str, 
                  password: str,
                  verbose: bool) -> MySqlDbScanner:
  
  return MySqlDbScanner(detectors, sample_size, url, db_name, username, password, verbose)
