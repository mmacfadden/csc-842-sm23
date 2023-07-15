from .data_detector import DataDetector
from .abstract_database_scanner import AbstractDatabaseScanner, TableDetections
import csv
import os
from typing import Optional

class AbstractSqlScanner(AbstractDatabaseScanner):

  def __init__(self, 
               detectors: list[DataDetector],
               sample_size: int,
               url: str,
               db_name: str,
               username: str,
               password: str,
               verbose: bool) -> None:
    super().__init__(detectors, sample_size, url, db_name, username, password, verbose)


  def scan(self, extract_dir: Optional[str]) -> list[TableDetections]:
    detections = []

    with self._create_connection() as connection:
    
      table_names = self._get_table_names(connection)

      for table in table_names:
        table_detections = self._scan_table(connection, table)
        if table_detections != None:
          detections.append(table_detections)
          if extract_dir != None:
            self._extract(connection, extract_dir, table_detections)
    
    return detections


  def _extract(self, connection, base_dir: str, detection: TableDetections) -> None:
    extract_query = f"SELECT * FROM {detection.table}"
    column_names = self._get_column_names(connection, detection.table)

    os.makedirs(base_dir, exist_ok=True)
    out_file = os.path.join(base_dir, f"{detection.table}.csv")
    with open(out_file,"w") as out:
      wr = csv.writer(out, quoting=csv.QUOTE_ALL)
      wr.writerow(column_names)

      with connection.cursor() as cursor:
        cursor.execute(extract_query)
        for row in cursor:
          wr.writerow(row)
 
  def _scan_table(self, connection , table) -> TableDetections:
    detections = {}
    
    select_query = f"SELECT * FROM {table} LIMIT 5"
    with connection.cursor() as cursor:
      cursor.execute(select_query)
      for row in cursor:
        for value in row:
          new_detections = self._scan_value(value)
          for nd in new_detections:
            if not nd.name in detections:
              detections[nd.name] = nd
            
    return TableDetections(table, detections.values())
  

  def _get_table_names(self, connection) -> list[str]:
    raise Exception("subclasses must override _get_table_names")
  
  def _get_column_names(self, connection, table) -> list[str]:
    raise Exception("subclasses must override _get_column_names")
  
  def _create_connection(self) -> any:
    raise Exception("subclasses must override _create_connection")