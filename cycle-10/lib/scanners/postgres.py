import psycopg2

from colorama import Fore, Style

from ..secret_detector import SecretDetector
from ..abstract_sql_scanner import AbstractSqlScanner
from ..util import fatal_error


class PostgresDbScanner(AbstractSqlScanner):

  def __init__(self, 
               detectors: list[SecretDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def _get_table_names(self, _) -> list[str]:
    raise Exception("subclasses must override _get_table_names")
  
  def _create_connection(self) -> any:
    if ":" in self.url:
      (host, port) = self.url.split(":")
    else:
      host = self.url
      port = 5432
  
    try:
      self._log(f"{Fore.YELLOW}Connecting to PostgreSQL{Style.RESET_ALL}: {host}:{port}")

      connection = psycopg2.connect(
        host=host,
        port=port,
        user=self.username,
        password=self.password,
        database=self.db_name)
      
      self._log(f"{Fore.GREEN}Successfully Connected.{Style.RESET_ALL}")

      return connection
    except Exception as e:
      fatal_error(f"Could not connect to PostgreSQL: {e}")
  

  def _get_table_names(self, connection) -> list[str]:
    table_names = []
    with connection.cursor() as cursor:
      cursor.execute("SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';")
      for table in cursor.fetchall():
        table_name = table[0]
        table_names.append(table_name)

    return table_names
  

def create_scanner(detectors: list[SecretDetector],
                  sample_size: int,
                  url: str, 
                  db_name: str, 
                  username: str, 
                  password: str,
                  verbose: bool) -> PostgresDbScanner:
  
  return PostgresDbScanner(detectors, sample_size, url, db_name, username, password, verbose)
